#!/usr/bin/python3

import boto3
from datetime import datetime, timedelta

REGIONS = ('us-west-1', 'us-east-1', 'us-west-2')
REGIONS_H = ('N. California', 'N. Virginia', 'Oregon')
do_not_delete_snapshots = ("snap-fcebd2d9", "snap-f641c8d5", "snap-cfdc3ff6", "snap-a3c04121", "snap-bf56579", "snap-3ff6c3be", "snap-441b05c5")

def get_AMIs():
    AMIs = list()
    for i in range(len(REGIONS)):
        region = REGIONS[i]
        region_h = REGIONS_H[i]
        rds = boto3.setup_default_session(region_name=region)
        rds = boto3.client('rds')

        ec2 = boto3.resource('ec2')
        images = ec2.images.filter(Owners=['self'])
        for image in images:
            AMIs.append(image.id)
    return AMIs

def get_snapshots():
    snapshots_list = list()
    for i in range(len(REGIONS)):
    #for i in range(2, 3):
        region = REGIONS[i]
        region_h = REGIONS_H[i]
        #print()
        #print("snapshots in {}".format(region_h))
        #print("--------------------------")

        ec2 = boto3.resource('ec2', region_name=region)
        snapshots = ec2.snapshots.filter()
        for snapshot in snapshots:
            if not snapshot.id in do_not_delete_snapshots:
            """            
            if snapshot.id in do_not_delete_snapshots:
                print("DO NOT DELETE: [{0}] ({1}, {2}, {3} {4} {5} {6})".format(snapshot.state, snapshot.volume_size, snapshot.volume_id, snapshot.id, snapshot.description, snapshot.start_time, snapshot.owner_id,),end="")
            else:
            """            
            #print("[{0}] ({1}, {2}, {3} {4} {5} {6})".format(snapshot.state, snapshot.volume_size, snapshot.volume_id, snapshot.id, snapshot.description, snapshot.start_time, snapshot.owner_id,),end="")
            #print("[{0}] ({1}, {2}, {3} {4} {5} {6})".format(region_h, snapshot.volume_size, snapshot.volume_id, snapshot.id, snapshot.description, snapshot.start_time, snapshot.owner_id,),end="")
            _line = str("[{0} {7}] ({1}, {2}, {3} {4} {5} {6})".format(region_h, snapshot.volume_size, snapshot.volume_id, snapshot.id, 
                                                                snapshot.description, snapshot.start_time, snapshot.owner_id, snapshot.state,))
            snapshots_list.append(_line)
        return snapshots_list
   
if __name__ == "__main__":
    AMIs = get_AMIs() 
    #print(len(AMIs), "AMIs:", AMIs)
    snapshots = get_snapshots()
    #for snapshot in snapshots:
    #    print(snapshot)
    print("\nfinding matches:\n")
    for snapshot in snapshots:
        for AMI in AMIs:
            if AMI not in snapshot:
                print("[no matching AMI found] for [{1}]".format(AMI, snapshot))
                break
            """
            else:
                print(">>>>>>>>>>>>>>>>>>>> [{0}] in [{1}]".format(AMI, snapshot))
            """
