import click
import picker
import adp_list
import draft

@click.command()
@click.option('--year', prompt='What year', help='')
@click.option('--draft_format', default='standard', help='')
@click.option('--rounds', default=15, help='')
@click.option('--teams', default=12, help='')
@click.option('--players', default=[], help='')
@click.option('--position', default=-1, help='')
def draft_app(year, draft_format, rounds, teams, players, position):
    """ app to simulate a fantasy football draft """

    adp_list = ADPList(year, teams, draft_format)

    if not players:
        players = create_players_list()

    board = draft(year, draft_format, rounds, teams, players, adp_list)

    board.export_table(#)

if __name__ == "__main__":
    draft_app()
