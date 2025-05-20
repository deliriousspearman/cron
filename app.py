from flask import Flask, render_template, request
from croniter import croniter
from datetime import datetime
import pytz

app = Flask(__name__)

def convert_cron_to_times(cron_expression, timezone):
    try:
        now = datetime.utcnow()  # Current UTC time
        cron = croniter(cron_expression, now)
        next_run = cron.get_next(datetime)  # Get next scheduled run
        
        selected_tz = pytz.timezone(timezone)
        utc = pytz.utc
        
        utc_time = utc.localize(next_run)
        selected_time = utc_time.astimezone(selected_tz)

        return {
            "UTC": utc_time.strftime('%Y-%m-%d %H:%M:%S %Z%z'),
            "Selected Timezone": selected_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')
        }
    except Exception as e:
        return {"error": str(e)}

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    timezones = pytz.all_timezones  # List of available timezones
    selected_timezone = "UTC"
    if request.method == 'POST':
        cron_expression = request.form['cron_expression']
        selected_timezone = request.form['timezone']
        result = convert_cron_to_times(cron_expression, selected_timezone)
    
    return render_template('index.html', result=result, timezones=timezones, selected_timezone=selected_timezone)

if __name__ == '__main__':
    app.run(debug=True)
