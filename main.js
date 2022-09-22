function createTblUsers() {
  const tbl = document.querySelector('#tbl-users')
  const head = document.createElement('thead')
  const body = document.createElement('tbody')
  body.id = 'tbl-users-body'
  const row = document.createElement('tr')
  const headers = ['name', 'code']

  removeChildren(tbl)

  for (const header of headers) {
    const headerElement = document.createElement('th')
    headerElement.innerText = header
    row.append(headerElement)
  }

  head.append(row)
  tbl.append(head)
  tbl.append(body)
}

function createTblLogs() {
  const tbl = document.querySelector('#tbl-logs')
  const head = document.createElement('thead')
  const body = document.createElement('tbody')
  body.id = 'tbl-logs-body'
  const row = document.createElement('tr')
  const headers = ['date', 'time', 'name']

  removeChildren(tbl)

  for (const header of headers) {
    const headerElement = document.createElement('th')
    headerElement.innerText = header
    row.append(headerElement)
  }

  head.append(row)
  tbl.append(head)
  tbl.append(body)
}

function removeChildren(element) {
  while (element.firstChild) {
    element.removeChild(element.lastChild)
  }
}

function initWS(websocket) {
  websocket.addEventListener("open", () => {
    let event = { type: "init" }
    websocket.send(JSON.stringify(event))
  })
}

function showMessage(message) {
  window.setTimeout(() => window.alert(message), 50)
}

function receiveMsg(websocket) {
  websocket.addEventListener("message", ({ data }) => {
    const event = JSON.parse(data)
    console.log(event)
    for (const user of event.users) {
      const body = document.querySelector('#tbl-users-body')
      const row = document.createElement('tr')
      const name = document.createElement('td')
      name.innerText = user[0]
      row.append(name)
      const code = document.createElement('td')
      code.innerText = user[1]
      row.append(code)
      body.append(row)
    }
    for (const log of event.logs) {
      const body = document.querySelector('#tbl-logs-body')
      const row = document.createElement('tr')
      const date = document.createElement('td')
      date.innerText = log[0]
      row.append(date)
      const time = document.createElement('td')
      time.innerText = log[1]
      row.append(time)
      const name = document.createElement('td')
      name.innerText = log[2]
      row.append(name)
      body.append(row)
    }
  })
}

window.addEventListener('DOMContentLoaded', () => {
  const btnUsers = document.querySelector('#btn-users')
  const btnLogs = document.querySelector('#btn-logs')
  const contUsers = document.querySelector('#cont-users')
  const contLogs = document.querySelector('#cont-logs')
  const tblLogs = document.querySelector('#tbl-logs')
  btnUsers.addEventListener('click', () => {
    btnUsers.classList.add('active')
    contUsers.classList.remove('d-none')
    btnLogs.classList.remove('active')
    contLogs.classList.add('d-none')
  })
  btnLogs.addEventListener('click', () => {
    btnUsers.classList.remove('active')
    btnLogs.classList.add('active')
    contUsers.classList.add('d-none')
    contLogs.classList.remove('d-none')
  })
  createTblUsers()
  createTblLogs()

  const websocket = new WebSocket("ws://localhost:8001/")
  initWS(websocket)
  receiveMsg(websocket)
})
