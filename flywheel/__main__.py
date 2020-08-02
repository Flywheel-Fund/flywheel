import click 

from flywheel.utils.google import GoogleService

@click.command()
@click.option('--email', default=False, help='if set, will trigger email')
@click.option('--debug', default=False, help='if set, will enable debug information')
def cli(email, debug):
    # Get stock data
    # Generate signals
    # Backtesting done offline
    # Based on threshold from backtesting, decide buy/sell signal
    # Send email
    if email:
        GoogleService().send_mail('')

if __name__ == '__main__':
    cli() # pylint: disable=no-value-for-parameter