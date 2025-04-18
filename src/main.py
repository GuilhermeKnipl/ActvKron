from datetime import datetime
#import numpy as np
import click 
from session import * 


@click.command()
@click.option("-start",is_flag= True, help="Start A Session")
@click.option("-end", is_flag = True, help= "End Your Session")
@click.option("-status", is_flag = True)
#@click.argument("")
def cli(start, end, status):
    
    dtnow = datetime.now()

    fmt_dtnow = format_dt(dt=dtnow) 
    if check_status() == False :
        if start:
            click.secho("\n Insert you activity details 📝", bold=True)
        

            session:Session = session_builder()
            session_summary(session)
            click.secho(f'\nStarting session at: {fmt_dtnow}', fg="green", bold=True)
            session.start_save()
            session.init()
        elif end:
            click.secho("\n   ####################################" ,bold = False)
            click.secho("   # Doesn\'t have any session running #", fg= "bright_white", bold =True)
            click.secho("   ####################################\n", bold = False)
    elif check_status() == True & end:
        end_session()
       
    elif check_status() == True & end == False: 
        click.secho("\n -- A Session is already Running --" , fg="red", bold=True)
        click.secho("End your last session before starting another\n", fg="red", bold=False)
    
    if status == True:
        session_stats()
    



if __name__ == "__main__":
    cli()
    
