function createTbl(tbl, headers) {
  const head = tbl.createTHead()
  const body = tbl.createTBody()
  body.id = tbl.id + '-body'
  const headRow = head.insertRow(-1)
  for (const header of headers) {
    const cell = document.createElement('th')
    cell.innerText = header
    headRow.append(cell)
  }
}

function initWS(websocket) {
  websocket.addEventListener("open", () => {
    let event = { type: "init" }
    websocket.send(JSON.stringify(event))
  })
}

function receiveMsg(websocket) {
  websocket.addEventListener("message", ({ data }) => {
    const event = JSON.parse(data)
    tblData.users = event.users
    tblData.logs = event.logs

    for (const user of tblData.users) {
      const body = document.querySelector('#tbl-users-body')
      const row = body.insertRow(-1)
      const name = row.insertCell(-1)
      name.innerText = user[0]
      const code = row.insertCell(-1)
      code.innerText = user[1]
    }
    for (const log of tblData.logs) {
      const body = document.querySelector('#tbl-logs-body')
      const row = body.insertRow(-1)
      const date = row.insertCell(-1)
      date.innerText = log[0]
      const time = row.insertCell(-1)
      time.innerText = log[1]
      const name = row.insertCell(-1)
      name.innerText = log[2]
    }
  })
}

window.addEventListener('DOMContentLoaded', () => {
  const btnUsers = document.querySelector('#btn-users')
  const btnLogs = document.querySelector('#btn-logs')
  const contUsers = document.querySelector('#cont-users')
  const contLogs = document.querySelector('#cont-logs')
  const tblUsers = document.querySelector('#tbl-users')
  const tblLogs = document.querySelector('#tbl-logs')

  tblData = {
    users: [],
    logs: []
  }

  btnUsers.addEventListener('click', () => {
    btnUsers.classList.add('active')
    contUsers.classList.remove('d-none')
    btnLogs.classList.remove('active')
    contLogs.classList.add('d-none')
    k
  })
  btnLogs.addEventListener('click', () => {
    btnUsers.classList.remove('active')
    btnLogs.classList.add('active')
    contUsers.classList.add('d-none')
    contLogs.classList.remove('d-none')
  })

  const HEADERS = {
    users: ['name', 'code'],
    logs: ['date', 'time', 'name']
  }
  createTbl(tblUsers, HEADERS.users)
  createTbl(tblLogs, HEADERS.logs)

  const websocket = new WebSocket("ws://192.168.1.118:8001/")
  initWS(websocket)
  receiveMsg(websocket)
})
