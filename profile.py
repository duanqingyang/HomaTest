"""
Use m510 machines to evaluate RAMCloud Homa implementation.
"""

import geni.portal as portal
import geni.rspec.pg as RSpec
import geni.urn as urn
import geni.aggregate.cloudlab as cloudlab

pc = portal.Context()

images = [ ("UBUNTU16-64-STD", "Ubuntu 16.04") ]

types  = [ ("m510", "m510 (Intel Xeon-D)")]

chassis = range(1,13+1)

nodesNum = range(3,45+1)

pc.defineParameter("image", "Disk Image",
                   portal.ParameterType.IMAGE, images[0], images)

pc.defineParameter("type", "Node Type",
                   portal.ParameterType.NODETYPE, types[0], types)

pc.defineParameter("chassis", "Which chassis to request",
                   portal.ParameterType.INTEGER,1,chassis)

pc.defineParameter("nodesNum", "total number of nodes",
                   portal.ParameterType.INTEGER,3,nodesNum)

params = pc.bindParameters()

rspec = RSpec.Request()

lan = RSpec.LAN()
rspec.addResource(lan)

num_nodes = params.nodesNum

rc_aliases = ["rcmaster", "rcnfs"]
for i in range(num_nodes - 2):
    rc_aliases.append("rc%02d" % (i + 1))

for i in range(num_nodes):
    name = "ms%02d%02d" % (params.chassis, i + 1)
    rc_alias = rc_aliases[i]
    node = RSpec.RawPC(rc_alias)
    

    if rc_alias == "rcnfs":
        # Ask for a 200GB file system mounted at /shome on rcnfs
        bs = node.Blockstore("bs", "/shome")
        bs.size = "200GB"

    node.hardware_type = params.type
    node.disk_image = urn.Image(cloudlab.Utah,"emulab-ops:%s" % params.image)
    node.component_id = urn.Node(cloudlab.Utah, name)

    #node.addService(RSpec.Execute(
    #        shell="sh", command="sudo /local/repository/startup.sh"))

    rspec.addResource(node)

    iface = node.addInterface("eth0")
    lan.addInterface(iface)

pc.printRequestRSpec(rspec)
