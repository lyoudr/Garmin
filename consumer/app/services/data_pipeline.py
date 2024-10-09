from apache_beam.options.pipeline_options import PipelineOptions
from pydantic import BaseModel
from decimal import Decimal
import apache_beam as beam
import argparse


class BillReportModel(BaseModel):
    service: str
    cost: float
    company: str


def count_fee_and_save_to_db(element) -> None:
    from ..main import app
    company, total_cost = element
    tech_fee = Decimal(total_cost) * Decimal('0.05')  # Applying 5% Serving Fee
    discounted_cost = Decimal(total_cost) * Decimal('0.98')  # Appying 98% Discount
    print(
        f"company:{company}"
        f"total_cost:{total_cost}",
        f"discounted_cost:{discounted_cost}",
        f"tech_fee:{tech_fee}"
    )
    # Insert statement for Cassandra
    query = """
        INSERT INTO billing_report (company, total_cost, discounted_cost, tech_fee) 
        VALUES (%s, %s, %s, %s)
    """

    # Execute the query
    session = app.state.cassandra_session
    session.execute(query, (
        company, 
        total_cost, 
        discounted_cost, 
        tech_fee
    ))


def transform_and_save_data(billing_data: BillReportModel) -> None:
    # Composite Transformation -> Group the services by company and sum the total cost
    (
        billing_data
        # Map Phase `Map(k1, k2) → list(k2,v2)`
        | 'Group by Company' >> beam.Map(
            lambda billing: (billing.company, billing.cost)
        )
        # Reduce Phase `Reduce(k2, list(v2)) → list((k3, v3))`
        | 'Combine' >> beam.CombinePerKey(sum)
        # Save to DataBase
        | 'Count Several Fees and Save to DB' >> beam.Map(
            count_fee_and_save_to_db
        )
    )


# handle billing data
def handle_csv_billing_data(file_path: str, save_main_session=True):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input',
        dest='input',
        default='/Users/annmac/Code/Ann/garmin/consumer/app/billing_report.csv',  # Path to csv file
        help='Input file to process.'
    )
    beam_options = PipelineOptions(
        runner='DirectRunner'
    )
    
    with beam.Pipeline(options=beam_options) as pipeline:
        # Read data from the CSV file
        lines = pipeline | beam.io.ReadFromText(
            file_path,
            skip_header_lines=1
        )

        # Parse csv file for apache beam
        class ParseCSV(beam.DoFn):
            
            def process(self, element):
                import csv
                reader = csv.reader([element])
                row = next(reader)
                service, cost, company = row[:3]
                return [BillReportModel(
                    service=service, 
                    cost=float(cost), 
                    company=company
                )]
        
        # Apply the ParseCSV ParDo function to parse the CSV data
        billing_data = lines | beam.ParDo(ParseCSV())

        # Map/Reduce data, and save data
        transform_and_save_data(billing_data)
