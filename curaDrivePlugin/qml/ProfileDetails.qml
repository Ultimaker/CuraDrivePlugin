// Copyright (c) 2018 Ultimaker B.V.
import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Controls.Styles 1.4
import QtGraphicalEffects 1.0
import UM 1.1 as UM

Item
{
    id: profileDetails

    property var profile
    property var logoutCallback

    anchors.fill: parent

    Row
    {
        id: profileDetailsRow

        spacing: UM.Theme.getSize("default_margin").width * 2

        height: childrenRect.height
        width: childrenRect.width

        anchors.left: parent.left
        anchors.leftMargin: UM.Theme.getSize("default_margin").width * 3
        anchors.top: parent.top
        anchors.topMargin: UM.Theme.getSize("default_margin").height * 3

        Rectangle
        {
            id: profileImageMask
            width: 96
            height: 96
            radius: 20

            Image
            {
                id: profileImage
                anchors.fill: parent
                fillMode: Image.PreserveAspectFit
                source: profile.profile_image_url

                // make image rounded
                layer.enabled: true
                layer.effect: OpacityMask {
                    maskSource: Item {
                        width: profileImage.width
                        height: profileImage.height
                        Rectangle {
                            anchors.centerIn: parent
                            width: profileImage.width
                            height: profileImage.height
                            radius: Math.min(width, height)
                        }
                    }
                }
            }
        }

        Label
        {
            id: usernameLabel
            text: profile.username
            height: 96
            font: UM.Theme.getFont("large")
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
        }

        Button
        {
            id: logoutButton

            anchors.top: profileDetails.bottom

            onClicked: profileDetails.logoutCallback()

            contentItem: Text {
                id: logoutButtonText
                text: "Logout"
                color: UM.Theme.getColor("action_button_text")
                font: UM.Theme.getFont("action_button")
            }

            background: Rectangle {
                color: UM.Theme.getColor("action_button")
            }
        }
    }
}