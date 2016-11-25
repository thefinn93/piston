/*
This file is part of Piston.

Piston is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Piston is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Piston.  If not, see <http://www.gnu.org/licenses/>.
*/

self.addEventListener('push', function(event) {
  var notificationPromise = registration.pushManager.getSubscription().then((subscription) => {
    var headers = new Headers();

    var gcm_endpoint = subscription.endpoint.split("/");
    headers.append("X-Token", gcm_endpoint[gcm_endpoint.length-1]);

    var unreadRequest = fetch('/notifications/unread', {headers: headers}).then((response) => {
      if(response.status == 200) {
        response.json().then((data) => {makeNotification(data, self.registration);});
      } else {
        console.error("Failed to fetch unread notifications! This is proly bad!");
      }
    });
    return unreadRequest;
  });
  event.waitUntil(notificationPromise);
});

function makeNotification(data, registration) {
  if (data.error) {
    console.error('The API returned an error.', data.error);
    throw new Error();
  } else {
    data.notifications.forEach(function(notification) {
      console.log(notification);
      if(!notification.title) {
        new Error("No title for notification!");
      }
      notification.tag = 'piston-' + notification.id;
      registration.showNotification(notification.title, {
        body: notification.body,
        options: notification
      });
    });
  }
}

self.addEventListener('notificationclick', function(event) {
  event.notification.close();
  var windowOpen = new Promise(function(resolve, reject) { resolve(); });
  if(event.notification.data.url || event.notification.data.url !== null) {
    var url = event.notification.data.url;
    if(event.action) {
      url = url + "?action=" + event.action;
    }
    windowOpen = clients.openWindow(url);
  } else {
    windowOpen = clients.openWindow('/notifications/' + event.notification.data.id);
  }
  event.waitUntil(windowOpen.then(function() {
    return fetch('/notifications/read/' + event.notification.data.id, {credentials: 'include'});
  }));
});
