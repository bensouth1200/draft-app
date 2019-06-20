import click
import picker
import adp_list
import draft

@click.command()
@click.option('--year', prompt='What year:', help='What year to simulate a draft of')
@click.option('--draft_format', default='standard', help='What type of scoring will the simulated draft be? (standard, half-ppr, ppr)')
@click.option('--rounds', default=15, help='How many rounds in the draft')
@click.option('--teams', default=12, help='How many teams in the draft')
@click.option('--players', default=[], help='An array of the types of pickers')
@click.option('--position', default=-1, help='Position that you wish to draft from')
def draft_app(year, draft_format, rounds, teams, players, position):
    """ app to simulate a fantasy football draft """

    adp_list = ADPList(year, teams, draft_format)

    if not players:
        players = create_players_list()

    board = draft(year, draft_format, rounds, teams, players, adp_list)

    board.export_table(#)

if __name__ == "__main__":
    draft_app()
