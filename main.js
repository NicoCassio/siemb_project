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

    const tblUsersBody = document.querySelector('#tbl-users-body')
    while (tblUsersBody.rows.length !== 0) {
      tblUsersBody.deleteRow(-1)
    }
    for (const user of tblData.users) {
      const row = tblUsersBody.insertRow(-1)
      const name = row.insertCell(-1)
      name.innerText = user.name
      const code = row.insertCell(-1)
      code.innerText = user.code

      const edit = row.insertCell(-1)
      const btnEdit = document.createElement('button')
      btnEdit.classList.add('btn')
      btnEdit.classList.add('btn-sm')
      btnEdit.setAttribute('data-bs-toggle', 'modal')
      btnEdit.setAttribute('data-bs-target', '#edit-modal')
      btnEdit.addEventListener('click', () => {
        const userId = document.querySelector('#user-id')
        userId.innerText = user.id
        const inputName = document.querySelector('#floating-input-name')
        inputName.value = user.name
        const inputCode = document.querySelector('#floating-input-code')
        inputCode.value = user.code
      })
      const imgEdit = document.createElement('img')
      imgEdit.src = './pencil-square.svg'
      imgEdit.width = '16'
      imgEdit.height = '16'
      btnEdit.append(imgEdit)
      edit.append(btnEdit)

      const del = row.insertCell(-1)
      const btnDel = document.createElement('button')
      btnDel.classList.add('btn')
      btnDel.classList.add('btn-sm')
      btnDel.setAttribute('data-bs-toggle', 'modal')
      btnDel.setAttribute('data-bs-target', '#delete-modal')
      btnDel.addEventListener('click', () => {
        const userId = document.querySelector('#del-user-id')
        userId.innerText = user.id
        const delName = document.querySelector('#delete-name')
        delName.innerText = user.name
      })
      const imgDel = document.createElement('img')
      imgDel.src = './trash.svg'
      imgDel.width = '16'
      imgDel.height = '16'
      btnDel.append(imgDel)
      del.append(btnDel)
    }

    const tblLogsBody = document.querySelector('#tbl-logs-body')
    while (tblLogsBody.rows.length !== 0) {
      tblLogsBody.deleteRow(-1)
    }
    for (const log of tblData.logs) {
      const body = document.querySelector('#tbl-logs-body')
      const row = body.insertRow(-1)
      const date = row.insertCell(-1)
      date.innerText = log.date
      const time = row.insertCell(-1)
      time.innerText = log.time
      const name = row.insertCell(-1)
      name.innerText = log.name
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
    contUsers.classList.remove('d-none')
    contLogs.classList.add('d-none')
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

  const btnAdd = document.querySelector('#btn-add')
  btnAdd.addEventListener('click', () => {
    const event = {
      type: 'add',
      user: {
        name: document.querySelector('#add-input-name').value,
        code: document.querySelector('#add-input-code').value
      }
    }
    websocket.send(JSON.stringify(event))

  })

  const btnSave = document.querySelector('#btn-save')
  btnSave.addEventListener('click', () => {
    const event = {
      type: 'edit',
      user: {
        id: document.querySelector('#user-id').innerText,
        name: document.querySelector('#floating-input-name').value,
        code: document.querySelector('#floating-input-code').value
      }
    }
    websocket.send(JSON.stringify(event))
  })

  const btnDelYes = document.querySelector('#btn-del-yes')
  btnDelYes.addEventListener('click', () => {
    const event = {
      type: 'delete',
      user: {
        id: document.querySelector('#del-user-id').innerText,
      }
    }
    websocket.send(JSON.stringify(event))
  })
})
