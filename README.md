python-whatpulse
================

This is a python wrapper around the [Whatpulse API][1].

Example Usage
-------------
```python
import whatpulse

api = whatpulse.API()
my_stats = api.get_user(192249)

print my_stats['AccountName']
print 'Total Keys: {0} (rank {1})'.format( my_stats['Keys'], my_stats['Ranks']['Keys'])
print 'Total Clicks: {0} (rank {1})'.format( my_stats['Clicks'], my_stats['Ranks']['Clicks'])
```

License
--------
Licensed under MIT License. See `LICENSE` for details.

[1]: http://www.whatpulse.org/pages/webapi/
