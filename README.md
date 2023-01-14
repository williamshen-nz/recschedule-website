# recschedule-website
See https://shen.nz/badminton for live website.

Parses the Open Rec Schedule PDF from MIT's website (https://www.mitrecsports.com/work-out/open-recreation/)
and generates a filtered version with Badminton. Since the PDF URL changes based on the date,
we scrape the website to get the URL in the [get_latest_recschedule.py](get_latest_recschedule.py) script.

**Note:** only badminton is supported for now but it should be easy to extend to other sports.

### Installation
Python 3.6+ required. Bash script was tested on Ubuntu 18.04 and Mac OS.

1. Install `pdftotext` if you don't have it installed already `sudo apt-get install poppler-utils`
2. Install the requirements `pip install -r requirements.txt`
3. Test the script by running `./run.sh`
4. If it all works, you can install a `crontab` to run the script periodically. See example below.

You may need to modify the `run.sh` script to work for your system with the relative paths, Python versions, etc.

```
# Run every 30 minutes and output to log
*/30 * * * * cd /home/willshen/recschedule-website && ./run.sh >> run.log 2>&1
```

### TODOs
Contributions are very welcome!

- [ ] Fix font-boosting issue on Android Chrome
- [ ] Change Tooltip color on dark mode to be more visible
