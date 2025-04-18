import os.path
from uuid import uuid4
from datetime import datetime 
from dataclasses import asdict, dataclass 
import json
import click

DATA_PATH = "data/session.json"
STATUS_PATH = "data/status.json"

@dataclass
class Session:
    id: str 
    start: str 
    end: str| None
    main_category: str
    category: str
    active: bool
    

    def save(self):
        session_data = asdict(self)
        session_data.pop('active')
        tries = 0
        while tries < 2:
            tries += 1

            if os.path.isfile(DATA_PATH): 
                with open(DATA_PATH, "r") as f:
                    try:
                        sessions = json.load(f)
                    except:
                        sessions = []
                    sessions.append(session_data)
                with open(DATA_PATH,"w") as f:
                    json.dump(sessions, f, indent=4, default=str)
        
                break
            else:
                try:
                    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)  
                    with open(DATA_PATH, 'w') as f:
                        json.dump([session_data], f, indent=4, default=str)  
                    break  

                except Exception as err:
                    print(f"Error creating the file {DATA_PATH}: {err}")
                    break

    def init(self):
        os.makedirs(os.path.dirname(STATUS_PATH), exist_ok=True)  

        status_data = {
                "session_id": self.id,
                "is_active": True
                }

        try:
            with open(STATUS_PATH, "w") as f:
                json.dump(status_data, f, indent=1)
        except Exception as err:
            print(err)


def format_dt(dt:datetime,pprint:bool = False ) -> str:
    if (pprint):
        return dt.strftime("Date: %Y-%m-%d \nTime: %H:%M:%S")
    else:
        return dt.strftime("%Y-%m-%d %H:%M:%S")



def session_summary(session: Session):
    click.secho(f"\nSession Id: {session.id}", fg="yellow", bold=True)
    click.secho(f"\n{session.start}", fg="cyan", bold=True)
    click.secho(f"\nMain Category: {session.main_category}", fg="bright_blue", bold=True)


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
    
    session: Session = Session(id=str(uuid4()), category=subcatg, main_category=main_catg
                               , start=start, end= None)
    session.init() 
    return session




