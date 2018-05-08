// Copyright (c) 2018 Ultimaker B.V.
import QtQuick 2.7
import QtQuick.Controls 2.1
import QtGraphicalEffects 1.0

Item
{
    id: icon
    width: parent.height
    height: width
    property var color: "transparent"
    property var iconSource

    Image
    {
        id: iconImage
        width: parent.height
        height: width
        smooth: true
        source: icon.iconSource
        sourceSize.width: width
        sourceSize.height: height
    }

    ColorOverlay
    {
        anchors.fill: iconImage
        source: iconImage
        color: icon.color
    }
}
