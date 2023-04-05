# What's in this directory
1. Demo.postman_collection.json - Collection used in the SP Network Champions Bootcamp
2. Demo.postman_environment.json - Sanitized evnironment for the SP Network Champions Bootcamp.  Modify the variables here to align with your controller and devices.
3. ND.postman_collection.json - A minimal set of Nexus Dashboard endpoints (enough to login, basically).  Use the NDFC Environment with this.
4. NDFC.postman_collection.json - A more complete set of endpoints for NDFC, which match the documentation. This is a work in progress (see below).
5. NDFC.postman_environment.json - The environment to use with both the NDFC and ND collections.  Modify this to match your local controller/switches.

# How long with these files be here?

At least a couple months from today (2023.04.05, April 5th...).  The NDFC and ND Postman collections herein will move to separate git repositories when they are more complete.  When this happens, I'll update this README.md file to point to the new locations.

# How to I use these files?

In Postman, click File -> Import (or click the "Import" button in the "My Workspace" pane on the left side of the GUI)

The *.postman_collection.json files will show up in the Collections tab (left side of the Postman GUI).
The *.postman_environment.json files will show up in the Environments tab (again, left side of the Postman GUI).

After importing, select the "Demo" environment from the drop-down menu at the top right of the Postman GUI if you're using the Demo collection.  Similarly, select the NDFC enviroment if you're using the ND or NDFC collections.

