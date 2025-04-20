import os.path
from uuid import uuid4
from datetime import date, datetime 
from dataclasses import asdict, dataclass 
import json
import click

STATUS_PATH = os.path.expanduser('~/desktop/ActvKron/data/status.json')
DATA_PATH = os.path.expanduser("~/desktop/lynx/ActvKron/data/session.json")

@dataclass
class Session:
    id: str 
    start: str 
    end: str| None
    main_category: str
    category: str
    active: bool
    duration: str | None

    def start_save(self):
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

def check_status() -> bool:

    with open(STATUS_PATH) as f:
      status = json.load(f)
      return status['is_active']

def end_session():
    with open(STATUS_PATH, 'r') as f:
        status = json.load(f)
        current_id = status['session_id']

    with open(DATA_PATH, 'r') as f:
        sessions = json.load(f)
        for s in sessions:
            if s['id'] == current_id:
                s["end"] = format_dt(datetime.now())
                end_time = datetime.strptime(s['end'], "%Y-%m-%d %H:%M:%S")
                start_time = datetime.strptime(s['start'],"%Y-%m-%d %H:%M:%S")
                duration = str(end_time - start_time)
                s["duration"] = duration 
                click.secho(f"\nSession endend with {s["duration"]}", fg="green", bold=True)

    with open(DATA_PATH, 'w') as fw:
        json.dump(sessions, fw , indent=4 )

    status_data = {
             "session_id": "0",
             "is_active": False
             }

    with open(STATUS_PATH, "w") as f:
            json.dump(status_data, f, indent=1)
        

def session_stats():

    with open(STATUS_PATH, "r") as f:
        data = json.load(f)
        current_id = data['session_id']
        status = data['is_active']
        if status:
            with open(DATA_PATH, 'r') as f:
                    sessions = json.load(f)
            for s in sessions:
                if s['id'] == current_id:
                    now_dt = format_dt(datetime.now())
                    time_now = datetime.strptime(now_dt, "%Y-%m-%d %H:%M:%S")
                    start_time = datetime.strptime(s['start'],"%Y-%m-%d %H:%M:%S")
                    duration = str(time_now - start_time)

                    click.secho("----------------------", fg="blue", bold=False)
                    click.secho("Session Is Running", fg="blue", bold=True)
                    click.secho(f"Session Time: {duration}", fg="blue", bold=True)
                    click.secho("----------------------", fg="blue", bold=False)

        else: 
            click.secho("Session Ended", fg="blue", bold=True)


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
    
    session: Session = Session(id=str(uuid4())
                               ,category=subcatg
                               ,main_category=main_catg
                               ,start=start
                               ,end=None
                               ,active= True
                               ,duration = None)
    
    return session





