# Ansible Role for File and Directory Exporter for Prometheus
This is a Exporter for monitoring files and directories with prometheus.  


Role Variables
--------------

`file_directory_exporter_working_dir`  
Working Directory
```yaml
file_directory_exporter_working_dir: "/opt/file_directory_exporter"
``` 

`file_directory_exporter_user`  
user
```yaml
file_directory_exporter_user: root
``` 

`file_directory_exporter_group`  
group
```yaml
file_directory_exporter_group: root
``` 

`file_directory_exporter_listen_address`  
Listening Address
```yaml
file_directory_exporter_listen_address: 0.0.0.0
``` 

`file_directory_exporter_listen_port`  
Listening Port
```yaml
file_directory_exporter_listen_port: 9101
``` 

`file_directory_exporter_files`  
List of individual files to monitor
```yaml
file_directory_exporter_files:
  - "/etc/fstab"
  - "/etc/network/interfaces"
  - "/etc/baum"
  - "/root/test"
  - "/etc/"
``` 

`file_directory_exporter_directories`  
List of directories to monitor
```yaml
file_directory_exporter_directories:
  - "/etc"
  - "/home/pi/"
  - "/app"
``` 

Example Playbook
----------------


```yaml

- hosts: servers
  roles:
    - role: ansible-role-file-directory-exporter
      file_directory_exporter_files:
        - "/opt/app1/file.zip"
        - "/opt/app2/file.zip"
      file_directory_exporter_directories:
        - "/opt/app3"
        - "/opt/app4"
``` 



### Example output
```
# file exporter for prometheus

# file checks for /etc/fstab
file_exist{file="/etc/fstab"} 1
file_age_seconds{file="/etc/fstab"} 1554719154
file_size_bytes{file="/etc/fstab"} 314

# file checks for /etc/network/interfaces
file_exist{file="/etc/network/interfaces"} 1
file_age_seconds{file="/etc/network/interfaces"} 1554717550
file_size_bytes{file="/etc/network/interfaces"} 271

# file checks for /etc/baum
file_exist{file="/etc/baum"} 0

# file checks for /root/test
file_exist{file="/root/test"} 0

# file checks for /etc/
file_exist{file="/etc/"} 0


# directory exporter for prometheus

# directory checks for /etc/
directory_exist{directory="/etc/"} 1
directory_contains_elements_number{"directory=/etc/"} 181
directory_contains_files_oldest{directory="/etc/"} 1494877532
directory_contains_files_newest{directory="/etc/"} 1627082059
directory_contains_files_smallest{directory="/etc/"} 9
directory_contains_files_bigest{directory="/etc/"} 549343

# directory checks for /home/pi/
directory_exist{directory="/home/pi/"} 1
directory_contains_elements_number{"directory=/home/pi/"} 8
directory_contains_files_oldest{directory="/home/pi/"} 1494844321
directory_contains_files_newest{directory="/home/pi/"} 1627082099
directory_contains_files_smallest{directory="/home/pi/"} 20
directory_contains_files_bigest{directory="/home/pi/"} 449543

# directory checks for /app
directory_exist{directory="/app"} 0
```

### FAQ
Q: What if the user that executes the exporter have no permissions for a file/directory?  
A: The file/directory will be displayed as non-existent.

Q: Which elements will the directory exporter count?  
A: Files, hidden files and directories (except `.` and `..`)

Q: Does the file age means the point of creation or the point of the last modification.  
A: It will display the timespan until the last point of modification (in seconds). You may read Python3 docs for [`os.path.getmtime()`](https://docs.python.org/3/library/os.path.html#os.path.getmtime).

Q: How to update the exporter?  
A: Go to the directory of the exporter and run `git pull` and `systemctl restart file_directory_exporter.service`.

Q: What if the config file could not be found?  
A: The exporter will stop directly after starting with exit code 1.

Q: What if i dont want to scan directories, just files? (or vice versa)  
A: Just remove all entries in the respective section (but dont remove the complete section) in the config file.

Q: Does this exporter also run on windows?  
A: Yes. But keep in mind to change the paths in the config file. Hint: Use / instead of \ in windows paths.

