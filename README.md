# morse-appstakes-tools
A set of tools and scripts to help Pocket Gateways manage Appstakes (Gigastakes)

## Overview
`morse-appstakes-tools` is a python tool that allows a user to quickly understand the state of existing Appstakes as well as manipulate Appstakes including Upstaking and TODO: Restaking. The tool is designed to be used as a bulk tool. Simply populate the `INPUTFILE` in your `.env` with a set of Appstakes addresses, and the script will process based on your input arguments. 

## Dependencies
Use of these tools require the following dependencies:
* `python3`
* `pip` 
* [`pocket-core`](https://github.com/pokt-network/pocket-core)

## Assumptions
This tool assumes the following:
* User has access to a Pocket Endpoint. Mint a free endpoint with [Grove](https://portal.grove.city)
* User has all private keys loaded into `pocket-core`
* User has set up all Appstake addresses with the same password and the same `datadir`
