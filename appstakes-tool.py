import argparse
import subprocess
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Read values from the .env file
input_file = os.getenv('INPUT_FILE')
output_file = os.getenv('OUTPUT_FILE')
remote_cli_url = os.getenv('REMOTE_CLI_URL')
datadir = os.getenv('DATADIR')
password = os.getenv('PASSWORD')

if not input_file or not output_file or not remote_cli_url:
    raise ValueError("INPUT_FILE, OUTPUT_FILE, and REMOTE_CLI_URL must be set in the .env file.")

# Define the function for the --info workflow (get balances with chains)
def get_pokt_balances(input_file, output_file, remote_cli_url):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        outfile.write("ADDRESS\tCHAINS\tSTAKED_TOKENS\n")  # Write the header row
        for line in infile:
            address = line.strip()
            if not address:
                continue # Skip empty lines
            try:
                # Run the pocket query command
                result = subprocess.run(
                    ['pocket', 'query', 'app', address, '--remoteCLIURL', remote_cli_url],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                output = result.stdout

                # Extract the JSON part of the output
                json_start = output.find('{')
                json_end = output.rfind('}') + 1
                if json_start == -1 or json_end == -1:
                    raise ValueError(f"Invalid output for address {address}: {output}")

                app_data = json.loads(output[json_start:json_end])

                # Extract necessary fields
                chains = ",".join(app_data.get('chains', []))
                staked_tokens = app_data.get('staked_tokens', '0')

                # Write to the output file
                outfile.write(f"{address}\t{chains}\t{staked_tokens}\n")
                print(f"✅ Processed: {address} - Chains: {chains} - Balance: {staked_tokens}")
            except Exception as e:
                print(f"❌ Error processing address {address}: {e}")

# Define the function for the --upstake workflow
# TODO: add ability to EXECUTE the commands after generating them, either with flag or with additional prompt
def upstake(input_file, output_file, remote_cli_url):
    additional_stake = input("Enter the additional stake amount (uPOKT): ")

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            address = line.strip()
            if not address:
                continue # Skip empty lines 
            try:
                # Run the pocket query command
                result = subprocess.run(
                    ['pocket', 'query', 'app', address, '--remoteCLIURL', remote_cli_url],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                output = result.stdout

                # Extract the JSON part of the output
                json_start = output.find('{')
                json_end = output.rfind('}') + 1
                if json_start == -1 or json_end == -1:
                    raise ValueError(f"Invalid output for address {address}: {output}")

                app_data = json.loads(output[json_start:json_end])

                # Extract necessary fields
                chains = ",".join(app_data.get('chains', []))
                staked_tokens = int(app_data.get('staked_tokens', '0'))

                # Calculate new stake amount
                new_stake = staked_tokens + int(additional_stake)

                # Write the upstake command to the output file
                outfile.write(
                    f"pocket apps stake {address} {new_stake} {chains} mainnet 10000 --remoteCLIURL {remote_cli_url} --datadir {datadir} --pwd {password}\n"
                )
                print(f"✅ Generated upstake command for {address} ")
            except Exception as e:
                print(f"❌ Error generating commands for address {address}: {e}")

# Main function to parse arguments and execute workflows
def main():
    parser = argparse.ArgumentParser(description="App Stakes Tool for Pocket Network Morse")
    parser.add_argument(
        '-u', '--upstake',
        action='store_true',
        help='Execute the upstake workflow. For each application address in the input file: Print to the output file the commands to upstake each application stake by the amount provided.'
    )
    parser.add_argument(
        '-i', '--info',
        action='store_true',
        help='Execute the info workflow. For each application address in the input file: returns the address, balance, and the currently staked chain IDs.'
    )

    args = parser.parse_args()

    if args.upstake:
        print("Executing upstake workflow...")
        upstake(input_file, output_file, remote_cli_url)
    elif args.info:
        print("Executing the info workflow...")
        get_pokt_balances(input_file, output_file, remote_cli_url)
    else:
        parser.print_help()

# Entry point
if __name__ == '__main__':
    main()
