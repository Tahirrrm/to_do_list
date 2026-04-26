const API_URL = 'http://localhost:3000/api'

let currentView = 'active'
let tasks = []

async function fetchTasks() {
  const res = await fetch(`${API_URL}/tasks?view=${currentView}`)
  tasks = await res.json()
  render()
}

async function addTask(title) {
  const res = await fetch(`${API_URL}/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title })
  })
  document.getElementById('addForm').reset()
  fetchTasks()
}

async function updateTask(id, data) {
  await fetch(`${API_URL}/tasks/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
  fetchTasks()
}

async function deleteTask(id) {
  await fetch(`${API_URL}/tasks/${id}`, { method: 'DELETE' })
  fetchTasks()
}

async function permanentDeleteTask(id) {
  await fetch(`${API_URL}/tasks/${id}/permanent`, { method: 'DELETE' })
  fetchTasks()
}

async function restoreTask(id) {
  await fetch(`${API_URL}/tasks/${id}/restore`, { method: 'POST' })
  fetchTasks()
}

function render() {
  const list = document.getElementById('taskList')
  const empty = document.getElementById('empty')

  list.innerHTML = ''
  empty.style.display = tasks.length ? 'none' : 'block'

  tasks.forEach(task => {
    const li = document.createElement('li')
    li.className = 'task'

    if (currentView === 'active') {
      li.innerHTML = `
        <span class="task-title">${task.title}</span>
        <div class="task-actions">
          <button class="btn-done" data-id="${task.id}" title="Выполнить">✓</button>
          <button class="btn-delete" data-id="${task.id}" title="В корзину">✕</button>
        </div>
      `
    } else if (currentView === 'done') {
      li.innerHTML = `
        <span class="task-title done">${task.title}</span>
        <div class="task-actions">
          <button class="btn-restore" data-id="${task.id}" title="Вернуть">↩</button>
          <button class="btn-delete" data-id="${task.id}" title="В корзину">✕</button>
        </div>
      `
    } else {
      li.innerHTML = `
        <span class="task-title trash">${task.title}</span>
        <div class="task-actions">
          <button class="btn-restore" data-id="${task.id}" title="Восстановить">↩</button>
          <button class="btn-delete permanently" data-id="${task.id}" title="Удалить навсегда">✕</button>
        </div>
      `
    }

    list.appendChild(li)
  })

  document.querySelectorAll('.tab').forEach(tab => {
    tab.classList.toggle('active', tab.dataset.view === currentView)
  })
}

document.getElementById('addForm').addEventListener('submit', e => {
  e.preventDefault()
  const input = e.target.querySelector('input')
  if (input.value.trim()) addTask(input.value.trim())
})

document.getElementById('taskList').addEventListener('click', e => {
  const id = parseInt(e.target.dataset.id)
  if (!id) return

  if (e.target.classList.contains('btn-done')) {
    updateTask(id, { status: 'done' })
  } else if (e.target.classList.contains('btn-delete') && !e.target.classList.contains('permanently')) {
    deleteTask(id)
  } else if (e.target.classList.contains('btn-restore')) {
    if (currentView === 'trash') {
      restoreTask(id)
    } else {
      updateTask(id, { status: 'active' })
    }
  } else if (e.target.classList.contains('btn-delete') && e.target.classList.contains('permanently')) {
    permanentDeleteTask(id)
  }
})

document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', () => {
    currentView = tab.dataset.view
    fetchTasks()
  })
})

fetchTasks()