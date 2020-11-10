# bnu_out.py
## Dependencies
Firefox
Firefox driver geckodriver
selenium (conda install)
argparse (pip install)

## Usage
python bnu_out.py [-h] [-work] [-play] [-diy]
Check out more by `python bnu_out.py -h`


# bnu_daka_mini.py
Mini version of w29593617/BNU-COVID19-Auto-Check-In. Everything about SMS is removed.

## Requirements
APScheduler>=3.6.0 (pip install)
requests>=2.22.0 (pip install)

## Usage
First modify config.txt then
python bnu_daka_mini.py

You can also edit crontab by `contab -e` then add the following line
0   7   *   *   *   /home/bnu/anaconda3/bin/python /home/bnu/bnufast/bnu_daka_mini.py >> /home/bnu/bnufast/bnu_daka_mini.log

This will check in for you everyday.
