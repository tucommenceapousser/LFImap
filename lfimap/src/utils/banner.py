import argparse
import pyfiglet
from termcolor import colored
import time
import sys

# Custom HelpFormatter
class BannerHelpFormatter(argparse.HelpFormatter):
    def __init__(self, prog):
        super().__init__(prog, max_help_position=30, width=100)

    def format_help(self):
        # Define a banner message using pyfiglet
        banner = pyfiglet.figlet_format("TRHACKNON", font="slant")
        banner_colored = colored(banner, 'cyan')

        # Add a bit of animation by displaying the banner letter by letter
        for char in banner_colored:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.005)

        # Display the byline with color
        byline = colored("                                - by @trhacknon\n\n\n", 'yellow')
        
        # Get the default help message
        help_text = super().format_help()

        # Return the animated banner followed by the byline and the help text
        return banner_colored + byline + help_text

# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=BannerHelpFormatter)
    parser.add_argument('--example', help='Just an example argument.')
    args = parser.parse_args()
