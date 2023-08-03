from dotenv import load_dotenv
import json
import ast
import click
load_dotenv(verbose=True, override=True)
del load_dotenv

@click.command()
@click.option("--instruction", '-i', default="What is the first prime number greater than 40 such that one plus the prime number is divisible by 3", help="Instruction to run")
def main(instruction: str):
    return

if __name__ == "__main__":
    main()
