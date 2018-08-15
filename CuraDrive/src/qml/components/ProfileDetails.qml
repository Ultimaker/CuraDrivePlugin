// Copyright (c) 2018 Ultimaker B.V.
import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.0

import UM 1.1 as UM

Item
{
    id: profileDetails
    property var profile
    property var logoutCallback
    height: childrenRect.height

    RowLayout
    {
        id: profileDetailsRow
        spacing: UM.Theme.getSize("default_margin").width * 2
        width: parent.width

        AvatarImage
        {
            width: 64
            height: width
            source: profile["profile_image_url"]
        }

        Label
        {
            text: profile["username"]
            font: UM.Theme.getFont("large")
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            Layout.alignment: Qt.AlignLeft
            Layout.fillWidth: true
            Layout.fillHeight: true
            renderType: Text.NativeRendering
        }

        ActionButton
        {
            text: catalog.i18nc("@button", "Manage Profile")
            color: "transparent"
            hoverColor: "transparent"
            textColor: UM.Theme.getColor("text")
            textHoverColor: UM.Theme.getColor("text_link")
            iconSource: "../images/home.svg"
            Layout.alignment: Qt.AlignRight
            onClicked: Qt.openUrlExternally("https://account.ultimaker.com")
        }

        ActionButton
        {
            text: catalog.i18nc("@button", "Sign Out")
            color: "transparent"
            hoverColor: "transparent"
            textColor: UM.Theme.getColor("text")
            textHoverColor: UM.Theme.getColor("text_link")
            Layout.alignment: Qt.AlignRight
            onClicked: profileDetails.logoutCallback()
        }
    }
}
