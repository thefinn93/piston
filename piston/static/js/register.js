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

function checkNotifications() {
  if('PushManager' in window && 'showNotification' in ServiceWorkerRegistration.prototype) {
    document.querySelector(".yes-notifications").classList.remove("hidden");
    document.querySelector(".no-notifications").classList.add("hidden");

    navigator.serviceWorker.register('/serviceworker.js');

    if(Notification.permission == "denied") {
      document.querySelector(".btn-allow").disabled = true;
      document.querySelector(".btn-allow").value = "Not Allowed";
    } else {
      document.querySelector(".btn-allow").disabled = false;
      document.querySelector(".btn-allow").value = "Allow";
    }
  } else {
    document.querySelector(".no-notifications").classList.remove("hidden");
    document.querySelector(".yes-notifications").classList.add("hidden");
  }
}

function onSubmit(e) {
  e.preventDefault();
  Notification.requestPermission().then((response) => {
    if(response == "granted") {
      navigator.serviceWorker.ready.then((serviceWorkerRegistration) => {
        serviceWorkerRegistration.pushManager.subscribe({userVisibleOnly: true}).then((subscription) => {
          document.querySelector("input[name='subscription']").value = JSON.stringify(subscription.toJSON());
          document.querySelector(".approval-form").submit();
        }).catch((e) => {
          var exception = Raven.captureException(e);
          console.log(e, exception);
        });
      });
    }
  }).catch((e) => {
    var exception = Raven.captureException(e);
    console.log(e, exception);
  });
}

function init() {
  checkNotifications();
  document.querySelector(".approval-form").addEventListener('submit', onSubmit);
}


init();
