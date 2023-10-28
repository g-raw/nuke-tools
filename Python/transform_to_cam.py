import nuke

def duplicate_node(node = None, new_node = None) : 
    if node == None :
        node = nuke.selectedNodes()

        node = node[0]

    node_class = node.Class()
    new_node = getattr(nuke.nodes, node_class)()

    for knob in new_node.knobs() :
        if knob == "name": continue
        new_node.knob(knob).fromScript(node.knob(knob).toScript())

    new_node.autoplace()

    return new_node

def transform_to_cam() :
    transform = nuke.selectedNodes('Transform')

    cam = nuke.selectedNodes('Camera')
    cam += nuke.selectedNodes('Camera2')
    cam += nuke.selectedNodes('Camera3')
    cam += nuke.selectedNodes('Camera4')
                                                                       
    trans_len = len(transform)
    cam_len = len(cam)

    if trans_len == 0 or cam_len == 0 :
        nuke.message('Select Transforms and Camera nodes')
        return

    elif trans_len > 1 or cam_len > 1 :
        nuke.message('Select max one Transform and one Camera')
        return

    transform_node_name = transform[0].name()
        
    #### Duplicating and renaming cam 
    track_cam = cam[0]
    conf_cam = duplicate_node(track_cam)
    conf_cam.knob('name').setValue('{}_CONFO_EDIT'.format(conf_cam.knob('name').value()))
    conf_cam.knob('read_from_file_link').setValue(0)

    #### Setting tranform links
    conf_cam.knob('win_translate').setExpression('-({0}.translate.x / ({0}.width/2))/{0}.scale.w+(1-(1/{0}.scale.w))*({0}.center.x/({0}.width/2)-1)'.format(transform_node_name), 0)
    conf_cam.knob('win_translate').setExpression('-({0}.translate.y / ({0}.width/2))/{0}.scale.h+(1-(1/{0}.scale.h))*({0}.center.y/({0}.height/2)-1)*({0}.height/{0}.width)'.format(transform_node_name), 1)
    conf_cam.knob('win_scale').setExpression("1/{}.scale.w".format(transform_node_name),0)    
    conf_cam.knob('win_scale').setExpression("1/{}.scale.h".format(transform_node_name),1) 

