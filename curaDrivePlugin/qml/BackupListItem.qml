// Copyright (c) 2018 Ultimaker B.V.
import QtQuick 2.7
import QtQuick.Controls 2.1

import UM 1.1 as UM

Rectangle
{
    id: backupListItem
    color: "blue"
    height: childrenRect.height

    Row
    {
        width: parent.width
        height: childrenRect.height
        spacing: Math.floor(UM.Theme.getSize("narrow_margin").width)

        Label
        {
            id: backupId
            text: model.backup_id
            width: parent.width
            height: UM.Theme.getSize("toolbox_property_label").height
        }
    }
}
