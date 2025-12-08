- Our users have expressed that they need to have finer grained control over the priority of tasks, instead of just
  urgent as a boolean, we should have a priority field with three values right now. HIGH, MEDIUM, and LOW, with
  HIGH > MEDIUM > LOW.
- We should have a small python migration script that can update an existing DB to use these new values.
- We should update our seed script to use this new value.
- We should update our server to take priority as a parameter.
- We should update our client.py to use this as a parameter.
