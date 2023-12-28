document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email());

  document.querySelector('#compose-form').onsubmit = send_email;

  // By default, load the inbox
  load_mailbox('inbox');
});



function compose_email(info = null, replying_to = { recipients: "", subject: "", body: "" , timestamp: ""}) {

  // clear out info message
  update_info(info);

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = replying_to.recipients;
  document.querySelector('#compose-subject').value = replying_to.subject;
  document.querySelector('#compose-body').value = replying_to.body;
}


function load_mailbox(mailbox, info = null) {

  update_info(info);

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  const emails_view = document.querySelector('#emails-view');
  console.log(`Fetching /emails/${mailbox}`)
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      //  if no emails, display message
      if (emails.length === 0) {
        update_info(`${mailbox} empty`);
        return;
      }

      // create table with space between rows
      const emails_table = document.createElement('table');

      // add bootstrap table classes
      emails_table.classList.add('table');
      emails_table.classList.add('table-hover');

      // create table header
      const table_header = document.createElement('thead');
      table_header.classList.add('thead-dark');
      const table_header_row = document.createElement('tr');
      table_header_row.innerHTML = '<th scope="col">From</th><th scope="col">Subject</th><th scope="col">Date and Time</th>';
      table_header.appendChild(table_header_row);

      // create table body
      const table_body = document.createElement('tbody');
      emails.forEach(email => {
        const table_row = document.createElement('tr')

        // table_row.classList.add('table-row-action');

        table_row.addEventListener('click', () => {
          console.log(`Clicked on email ${email.id}`);
          load_email(email.id, from_sent_box = (mailbox === "sent"));
        });

        table_row.innerHTML = `<td>${email.sender}</td><td>${email.subject}</td><td>${email.timestamp}</td>`;
        if (email.read) {
          table_row.classList.add('read');
        }
        table_body.appendChild(table_row);

      });

      emails_table.appendChild(table_body);
      emails_table.appendChild(table_header);
      emails_view.appendChild(emails_table);

    });
}

function load_email(email_id, from_sent_box) {

  update_info(`Loading email...`);
  console.log(`From sent box: ${from_sent_box}`)

  // Show the email and hide other views
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  
  // add fields to email view
  const subject_view = document.querySelector("#email-subject");
  const sender_view = document.querySelector("#email-sender");
  const recipients_view = document.querySelector("#email-recipients");
  const timestamp_view = document.querySelector("#email-timestamp");
  const body_view = document.querySelector("#email-body");
  subject_view.innerHTML = "";
  sender_view.innerHTML = "";
  timestamp_view.innerHTML = "";
  body_view.innerHTML = "";


  // mark email as read
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  });

  // get email
  const email_view = document.querySelector('#email-view');
  fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {
      console.log(email);
      subject_view.innerHTML = `<b> Subject: </b> ${email.subject}`;
      sender_view.innerHTML = `<b> From: </b> ${email.sender}`;
      recipients_view.innerHTML = `<b> To: </b> ${email.recipients.join(", ")}`;
      timestamp_view.innerHTML = `<b> Date and Time: </b> ${email.timestamp}`;
      body_view.innerHTML = `${email.body}`;

      // remove any existing buttons inside email view
      const buttons = document.querySelectorAll('#email-view button');
      buttons.forEach(button => button.remove());

      // add archive button 
      if (!from_sent_box === true) {
        // create archive button
        const archive_button = document.createElement('button');
        archive_button.classList.add('btn');
        archive_button.classList.add('btn-sm');
        archive_button.classList.add('btn-outline-primary');
        archive_button.innerHTML = email.archived ? "Unarchive" : "Archive";
        archive_button.addEventListener('click', () => {
          toggle_archive_email(email_id, email.archived);
          load_mailbox("inbox");
        });
        email_view.appendChild(archive_button);
      }

      // add reply button
      const reply_button = document.createElement('button');
      reply_button.classList.add('btn');
      reply_button.classList.add('btn-sm');
      reply_button.classList.add('btn-outline-primary');
      reply_button.innerHTML = "Reply";

      replying_to = {
        recipients: email.sender,
        subject: `Re: ${email.subject}`,
        body: `On ${email.timestamp} ${email.sender} wrote:\n\n${email.body}`
      }
      reply_button.addEventListener('click', () => {
        compose_email(
          info = `Replying to ${email.sender}`,
          replying_to = replying_to
        );
      });
      email_view.appendChild(reply_button);

    });


  update_info("");

}


function send_email() {

  // clear out info message
  update_info(null);

  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const mail_body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: mail_body
    })
  })
    .then(response => response.json())
    .then(result => {
      let info;
      if (result.error) {
        info = `Error: ${result.error}`;
        console.log(info);
        update_info(info);
      }
      else {
        info = `${result.message}`;
        load_mailbox("sent", info);
      }
    });

  return false;
}

function update_info(info = null) {
  document.querySelector("#info").innerHTML = info;
}

function toggle_archive_email(email_id, is_archived) {
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: !is_archived
    })
  });
  load_mailbox("inbox", "Email archived");
}