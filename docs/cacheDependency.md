# Cache Dependency

## Demo

<iframe src="https://vine.co/v/etgXVIPA7Yz/embed/simple" width="480" height="480" frameborder="0"></iframe><script src="https://platform.vine.co/static/scripts/embed.js"></script>

[Demo - Vine](https://vine.co/v/etgXVIPA7Yz)

## Procedure

1. Select nodes we want to chache out.
2. Excecute this tool.

## Behaviour

* Create File Cache SOP under the each selected node.
* Geometry ROP nodes that some parameter are referenced from File Cache SOP will be created under /out path as a dpendency is built.
* If you have already FileCache SOP in your network, this tool automatically uses that node when you selected.
