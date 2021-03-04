# TRUENAS_CONFIG_BACKUP

Small backup script for TrueNAS Scale. This script creates a backup of the system configuration. The target use-case for this script is to automate system configuration backups which include the `secretseed`, `pool_keys`, and the `root_authorized_keys`.

Creating a system backup can be done directly through the [TrueNAS Web UI](https://www.truenas.com/docs/hub/tasks/administrative/backup-config/).

## Details

The backup.py script is designed to be ran by the `root` user directly on the storage array. It does not support calling backup API remotely. The script uses the `middlewared` client module directly. The script needs access to the `middleware` sock file located in `/var/run/middleware.sock`. This bypasses the need to supply authentication credentials to create the backup.

## Usage

The primary use-case for backup.py is to be kicked off as a `pre-script` to a cloud-sync. The idea is to let this script run and generate a backup file then use a Cloud Sync job to encrypt and upload the configuration tar archive to a remote location. The `CLOUD_SYNC_PATH` environment variable set by the sync job controls the destination path for the backup file.

If the `CLOUD_SYNC_PATH` environment variable is not set, the script looks for `BACKUP_PATH`. Use `BACKUP_PATH` to control the location of the backup archive if running the script outside of a cloud sync job. The `/tmp` directory is the fallback if neither of the path environment variables are set.

The python3 interpretor used by the `middlewared` daemon should be used to run the script. This will ensure that the necessary python libraries are available. On TrueNAS SCALE, this is likely `/usr/bin/python3`.

### How to run

* Run as the `root` due to the middleware sock file being owned and grouped into `root`
* Use the python interpretor that has the middlwared python package installed. On my TrueNas SCALE install it is located at `/usr/bin/python3`
* Run as a pre-script for a cloud sync job. The `CLOUD_SYNC_PATH` environment variable , set by the sync job, will store the backups.
* Optionally run the script as a CRON job instead. Set the `BACKUP_PATH` environment variable to control where backups end up.