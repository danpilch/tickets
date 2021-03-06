import digitalocean
import argparse
import time
import os

class DOInstances(object):
    def __init__(self, instance_count, instance_region, server_prefix):
        # Get the api token from your account
        self.do_api_token = ""
        self.manager = digitalocean.Manager(token=self.do_api_token)
        self.instance_count = instance_count
        self.region = instance_region
        self.image_size = "512mb"
        self.server_prefix = server_prefix

    def get_images(self):
        images = self.manager.get_my_images()
        return(images)

    def create(self, image_id):
        print("Creating proxies")
        for instance in range(0, self.instance_count):
            print("Creating {!s}-{!s}-{!s}".format(self.server_prefix, self.region, instance))
            droplet = digitalocean.Droplet(token=self.do_api_token,
                    name = "{!s}-{!s}-{!s}".format(self.server_prefix, self.region, instance),
                    region = self.region,
                    image = image_id,
                    size_slug = self.image_size,
                    backups=False)

            new_droplet = droplet.create()
            
        print("Waiting for instance ip addresses to be allocated...")
        time.sleep(60)
        print("Outputting list of proxies:\n")
        droplets = self.manager.get_all_droplets()
        for droplet in droplets:
            if self.server_prefix in str(droplet):
                print("{!s}:9999".format(droplet.ip_address))

        print("Complete")

    def destroy(self):
        print("Destroying proxies: ")
        droplets = self.manager.get_all_droplets()
        for drop in droplets:
            if self.server_prefix in str(drop):
                print("destroying: {!s}".format(drop))
                drop.destroy()
        print("Complete")


def main():
    
    # Get current directory
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Argument parser
    parser = argparse.ArgumentParser(description="Automate generating Digitalocean proxy instances")
    parser.add_argument("--create", "-c", help="Create instances", action="store_true", required=False)
    parser.add_argument("--destroy", "-d", help="Destroy instances", action="store_true", required=False)
    parser.add_argument("--list", "-l", help="List snapshot images available", action="store_true", required=False)
    parser.add_argument("--instances", "-i", help="Number of instances to create", required=False, default=5, type=int)
    parser.add_argument("--region", "-r", help="Region to deploy instances to", required=False, default="lon1")
    parser.add_argument("--prefix", "-p", help="Prefix for server name", required=False, default="proxy")
    args = parser.parse_args()

    # Let's go
    run = DOInstances(instance_count=args.instances, instance_region=args.region, server_prefix=args.prefix)
    images = run.get_images()

    if args.create:
        run.create(images[0].id)
    elif args.destroy:
        run.destroy()
    elif args.list:
        for image in images:
            print(image)
    else:
        print("Doing nothing")


if __name__ == "__main__":
    main()
