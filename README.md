# recschedule-website

See https://shen.nz/badminton for live website.

Parses the Open Rec Schedule from MIT's Open Recreation Mazevo
Calendar: https://www.mitrecsports.com/work-out/open-recreation/

**Note:** only badminton is supported for now but it should be easy to extend to other sports.

### Installation

Python 3.6+ required. Bash script was tested on Ubuntu 18.04 and Mac OS.

1. Install the requirements `pip install -r requirements.txt`
2. Test the script by running `python main.py`
3. If it all works, you can install a `crontab` to run the script periodically. See example below.

```
# Run every 10 minutes and output to log
*/10 * * * * cd /home/willshen/recschedule-website && python main.py >> run.log 2>&1
```

### Issues

Contributions are very welcome! These issues might be out of date.

- [ ] [Fix font-boosting issue on Android Chrome](https://github.com/williamshen-nz/recschedule-website/issues/6)
- [ ] [Change Tooltip color on dark mode to be more visible](https://github.com/williamshen-nz/recschedule-website/issues/7)
