#!/bin/bash
rsync -av --exclude=.venv --exclude=.git --exclude=.ipynb* --exclude=__pycache__ --exclude=rsync_git.sh --exclude=.idea ~/workspace/quaternionphysics/Physics/Webapps/rotations_by_groups/ ~/Documents/Github/rotations_by_groups/
