# recschedule-website

Parses the `recschedule.pdf` from MIT's website (http://web.mit.edu/athletics/www/recschedule.pdf)
and generates a filtered version with Badminton.

See https://shen.nz/badminton for an example.

**Note:** only badminton is supported for now but should be easy to extend to other sports.

### Installation
Python 3.6+ required. Bash script was tested on Ubuntu 18.04.

1. Install `pdftotext` if you don't have it installed already `sudo apt-get install poppler-utils`
2. Install the requirements `pip install -r requirements.txt`
3. Test the script by running `./run.sh`
4. If it all works, you can install a `crontab` to run the script periodically. See example below.

You may need to modify the `run.sh` script to work for your system with the relative paths, Python versions, etc.

```
# Run every 30 minutes and output to log
*/30 * * * * /home/ubuntu/recschedule-website/run.sh >> /home/ubuntu/recschedule-website/run.log
```

### TODO
- Unit tests
- Test on more recschedules
- Manually verify against some schedules
