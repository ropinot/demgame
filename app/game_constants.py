
YES = 1
NO = 0

OK = 1
KO = 0

# Roles
ADMIN = 'admin'
PLAYER = 'player'

IDLE = 'IDLE'               # just after creation
ACTIVE = 'ACTIVE'           # waiting for players
RUNNING = 'RUNNING'         # running (!)
COMPLETED = 'COMPLETED'     # after run. Each scenario can be played once
ABORTED = 'ABORTED'         # if aborted (not used so far)
PAUSED = 'PAUSED'           # if interrupted manually and temporarily

SCENARIO_STATUSES = [IDLE, ACTIVE, RUNNING, COMPLETED, ABORTED, PAUSED]
