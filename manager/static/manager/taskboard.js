const draggables = document.querySelectorAll('.draggable')
const drop_areas = document.querySelectorAll('.drop_area')

draggables.forEach(draggable => {
  draggable.addEventListener('dragstart', () => {
    draggable.classList.add('dragging')
  })

  draggable.addEventListener('dragend', () => {
    draggable.classList.remove('dragging')
  })
})

drop_areas.forEach(drop_area => {
  drop_area.addEventListener('dragover', event => {
    event.preventDefault()
    const afterElement = getDragAfterElement(drop_area, event.clientY)
    const draggable = document.querySelector('.dragging')
    if (afterElement == null) {
      drop_area.appendChild(draggable)
    } else {
      drop_area.insertBefore(draggable, afterElement)
    }
  })
})

function getDragAfterElement(drop_area, y) {
  const draggableElements = [...drop_area.querySelectorAll('.draggable:not(.dragging)')]

  return draggableElements.reduce((closest, child) => {
    const box = child.getBoundingClientRect()
    const offset = y - box.top - box.height / 2
    if (offset < 0 && offset > closest.offset) {
      return { offset: offset, element: child }
    } else {
      return closest
    }
  }, { offset: Number.NEGATIVE_INFINITY }).element
}