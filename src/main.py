from datetime import datetime
from uuid import uuid4
#import numpy as np
import click 
from session import Session, format_dt, session_summary

def session_builder() -> Session:
    start = format_dt(datetime.now())
    main_catg = click.prompt(
            click.style(" - Main Category: ", fg="blue", bold= True)
            ,type=str 
        )
    subcatg = click.prompt(
            click.style("-- Subcategory: ", fg="bright_blue",bold=True)
            ,type=str
            )
    
    session: Session = Session(id=str(uuid4())
                               ,category=subcatg
                               ,main_category=main_catg
                               ,start=start
                               ,end=None
                               ,active= True)
    
    return session




@click.command()
@click.option("-init",is_flag= True, help="doesthis")
#@click.argument("")
def cli(init):
    
    dtnow = datetime.now()

    fmt_dtnow = format_dt(dt=dtnow) 
    if init:
        click.secho("\n Insert you activity details 📝", bold=True)
        

        session:Session = session_builder()
        session_summary(session)
        click.secho(f'\nStarting session at: {fmt_dtnow}', fg="green", bold=True)
        session.save()

        #click.echo(click.style("Warning!", fg="yellow"))


if __name__ == "__main__":
    cli()
    
