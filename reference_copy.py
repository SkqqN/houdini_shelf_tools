import hou

node = hou.selectedNodes()

for n in node:
    #Create Node
    reference = n.parent().createNode(n.type().name(), '{0}_refcopy'.format(n.name()))
    reference.setPosition(n.position())
    reference.move((0.5, -0.5))
    reference.setColor(hou.Color((0.38, 0.408, 0.553)))
    
    #Create Reference Parameter
    template = reference.parmTemplateGroup()
    help_text = 'Path to the source node whose is being referenced by this copy'
    new_parm = hou.StringParmTemplate('ref_path', 'Reference Path', 1, string_type=hou.stringParmType.NodeReference, help=help_text)
    template.insertBefore((0,), new_parm)
    reference.setParmTemplateGroup(template)
    reference.parm('ref_path').set(n.path())

    #Link parms
    for p in reference.parms():
        if p.name() == 'ref_path': #Skip Path Parameter : We don't want to affect the linked path
            continue
        if p.parmTemplate().type() == hou.parmTemplateType.Folder or p.parmTemplate().type() == hou.parmTemplateType.FolderSet:
            continue

        mode = kwargs['ctrlclick']
        if mode: #HScript
            expr = 'ch'
            if p.parmTemplate().type() == hou.parmTemplateType.String: #Adapt the expression to string parameters
                expr = 'chs'
            p.setExpression("{0}(chs('ref_path') + '/{1}')".format(expr, p.name()), hou.exprLanguage.Hscript)
            
        else: #Python
            p.setExpression("hou.node(hou.pwd().evalParm('ref_path')).evalParm('{0}')".format(p.name()), hou.exprLanguage.Python)
