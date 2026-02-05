/**
 * OpenFlex Neo - Drag and Drop Runtime
 * Flex-style DnD API mapped to HTML5 Drag and Drop
 */

// ============================================================
// DragSource - Container for dragged data (mx.core.DragSource)
// ============================================================
class DragSource {
  constructor() {
    this._data = {};
    this._formats = [];
  }

  addData(data, format) {
    this._data[format] = data;
    if (this._formats.indexOf(format) === -1) {
      this._formats.push(format);
    }
  }

  hasFormat(format) {
    return this._formats.indexOf(format) !== -1;
  }

  dataForFormat(format) {
    return this._data[format];
  }

  get formats() {
    return this._formats.slice();
  }
}

// ============================================================
// NeoFlexDragEvent - Wrapper over HTML5 DragEvent with Flex API
// ============================================================
class NeoFlexDragEvent {
  // Event type constants
  static DRAG_START = 'dragStart';
  static DRAG_ENTER = 'dragEnter';
  static DRAG_OVER = 'dragOver';
  static DRAG_EXIT = 'dragExit';
  static DRAG_DROP = 'dragDrop';
  static DRAG_COMPLETE = 'dragComplete';

  constructor(type, nativeEvent, dragSource, action, dragInitiator) {
    this.type = type;
    this.nativeEvent = nativeEvent;
    this.dragSource = dragSource || null;
    this.action = action || 'copy';
    this.dragInitiator = dragInitiator || null;
    this._insertIndex = -1;
  }

  get insertIndex() {
    return this._insertIndex;
  }
}

// ============================================================
// DragManager - Global singleton coordinator
// ============================================================
const DragManager = {
  _isDragging: false,
  _dragSource: null,
  _action: 'copy',
  _dragInitiator: null,

  get isDragging() {
    return this._isDragging;
  },

  /**
   * Initiate a drag operation (called from dragstart handler).
   * @param {HTMLElement} initiator - The element initiating the drag
   * @param {DragSource} dragSource - The data being dragged
   * @param {DragEvent} mouseEvent - The native dragstart event
   * @param {HTMLElement} [dragImage] - Custom drag image element
   * @param {number} [xOff] - X offset for drag image
   * @param {number} [yOff] - Y offset for drag image
   * @param {string} [action] - 'copy' or 'move'
   */
  doDrag(initiator, dragSource, mouseEvent, dragImage, xOff, yOff, action) {
    this._isDragging = true;
    this._dragSource = dragSource;
    this._action = action || 'copy';
    this._dragInitiator = initiator;

    // Serialize data to DataTransfer for cross-element communication
    if (mouseEvent && mouseEvent.dataTransfer) {
      var payload = {};
      dragSource.formats.forEach(function(fmt) {
        payload[fmt] = dragSource.dataForFormat(fmt);
      });
      try {
        mouseEvent.dataTransfer.setData('application/x-openflex-dnd', JSON.stringify(payload));
      } catch (e) {
        // Fallback for browsers that don't support custom MIME types
        mouseEvent.dataTransfer.setData('text/plain', JSON.stringify(payload));
      }
      mouseEvent.dataTransfer.effectAllowed = action === 'move' ? 'move' : 'copyMove';

      // Custom drag image if provided
      if (dragImage && mouseEvent.dataTransfer.setDragImage) {
        mouseEvent.dataTransfer.setDragImage(dragImage, xOff || 0, yOff || 0);
      }
    }
  },

  /**
   * End the current drag operation
   */
  endDrag() {
    this._isDragging = false;
    this._dragSource = null;
    this._dragInitiator = null;
  }
};

// ============================================================
// Drop Indicator helpers
// ============================================================

/**
 * Update the position of the drop indicator line inside a container.
 * @param {HTMLElement} container - The drop target container
 * @param {number} index - The insertion index (0-based)
 * @param {HTMLElement[]} children - Array of child elements
 */
function _updateDropIndicator(container, index, children) {
  // Find or create the indicator
  var indicator = container.querySelector('.neo-drop-indicator');
  if (!indicator) {
    indicator = document.createElement('div');
    indicator.className = 'neo-drop-indicator';
    container.appendChild(indicator);
  }

  indicator.style.display = 'block';

  // Position the indicator
  if (children.length === 0) {
    indicator.style.top = '0px';
  } else if (index >= children.length) {
    // After the last child
    var lastChild = children[children.length - 1];
    indicator.style.top = (lastChild.offsetTop + lastChild.offsetHeight) + 'px';
  } else {
    // Before the child at index
    indicator.style.top = (children[index].offsetTop - 1) + 'px';
  }
}

/**
 * Remove (hide) the drop indicator from a container.
 * @param {HTMLElement} container
 */
function _removeDropIndicator(container) {
  var indicator = container.querySelector('.neo-drop-indicator');
  if (indicator) {
    indicator.style.display = 'none';
  }
}

/**
 * Calculate the insertion index based on mouse Y position relative to children.
 * @param {HTMLElement} container
 * @param {number} clientY - Mouse Y coordinate
 * @param {HTMLElement[]} children - Array of draggable child elements
 * @returns {number} The insertion index
 */
function _calcInsertIndex(container, clientY, children) {
  for (var i = 0; i < children.length; i++) {
    var rect = children[i].getBoundingClientRect();
    var midY = rect.top + rect.height / 2;
    if (clientY < midY) {
      return i;
    }
  }
  return children.length;
}

// ============================================================
// setupDragSource - Called by compiler-generated code
// ============================================================

/**
 * Make an element draggable with Flex-style DnD.
 * @param {HTMLElement} element - The element to make draggable
 * @param {Object} options
 * @param {*} options.item - The data item this element represents
 * @param {number} options.index - The index of this item in its parent list
 * @param {string} [options.labelField] - Field name to use for label
 * @param {string} [options.action] - 'copy' or 'move' (default: 'copy')
 * @param {Function} [options.onDragStart] - Callback on drag start
 * @param {Function} [options.onDragComplete] - Callback on drag complete
 */
function setupDragSource(element, options) {
  if (!element || element._neoDragSourceBound) return;
  element._neoDragSourceBound = true;

  element.setAttribute('draggable', 'true');
  element.classList.add('neo-drag-enabled');

  element.addEventListener('dragstart', function(e) {
    var dragSource = new DragSource();
    dragSource.addData(options.item, 'items');
    dragSource.addData(options.index, 'index');

    var action = options.action || 'copy';

    // Create Flex-style event
    var flexEvent = new NeoFlexDragEvent(
      NeoFlexDragEvent.DRAG_START, e, dragSource, action, element
    );

    // Let user handler customize if needed
    if (typeof options.onDragStart === 'function') {
      options.onDragStart(flexEvent);
    }

    // Initiate through DragManager
    DragManager.doDrag(element, dragSource, e, null, 0, 0, action);

    // Visual feedback
    element.classList.add('neo-dragging');
  });

  element.addEventListener('dragend', function(e) {
    element.classList.remove('neo-dragging');

    var flexEvent = new NeoFlexDragEvent(
      NeoFlexDragEvent.DRAG_COMPLETE, e, DragManager._dragSource, DragManager._action, element
    );

    if (typeof options.onDragComplete === 'function') {
      options.onDragComplete(flexEvent);
    }

    DragManager.endDrag();
  });
}

// ============================================================
// setupDropTarget - Called by compiler-generated code
// ============================================================

/**
 * Make a container accept drops with Flex-style DnD.
 * @param {HTMLElement} element - The container element
 * @param {Object} options
 * @param {string} [options.childSelector] - CSS selector for droppable children (default: direct children minus indicator)
 * @param {Function} [options.onDragEnter] - Callback on drag enter
 * @param {Function} [options.onDragOver] - Callback on drag over
 * @param {Function} [options.onDragExit] - Callback on drag exit
 * @param {Function} [options.onDragDrop] - Callback on drop
 */
function setupDropTarget(element, options) {
  if (!element || element._neoDropTargetBound) return;
  element._neoDropTargetBound = true;

  element.addEventListener('dragenter', function(e) {
    e.preventDefault();
    element.classList.add('neo-drag-over');

    if (typeof options.onDragEnter === 'function') {
      var flexEvent = new NeoFlexDragEvent(
        NeoFlexDragEvent.DRAG_ENTER, e, DragManager._dragSource, DragManager._action
      );
      options.onDragEnter(flexEvent);
    }
  });

  element.addEventListener('dragover', function(e) {
    e.preventDefault(); // Required to allow drop
    e.dataTransfer.dropEffect = DragManager._action === 'move' ? 'move' : 'copy';

    // Calculate insert index and show indicator
    var selector = options.childSelector || '.neo-list-item, tr.neo-datagrid-row';
    var children = Array.from(element.querySelectorAll(':scope > ' + selector.split(',')[0].trim()));
    // Fallback: use direct non-indicator children
    if (children.length === 0) {
      children = Array.from(element.children).filter(function(ch) {
        return !ch.classList.contains('neo-drop-indicator');
      });
    }

    var insertIndex = _calcInsertIndex(element, e.clientY, children);
    _updateDropIndicator(element, insertIndex, children);

    if (typeof options.onDragOver === 'function') {
      var flexEvent = new NeoFlexDragEvent(
        NeoFlexDragEvent.DRAG_OVER, e, DragManager._dragSource, DragManager._action
      );
      flexEvent._insertIndex = insertIndex;
      options.onDragOver(flexEvent);
    }
  });

  element.addEventListener('dragleave', function(e) {
    // Only remove if actually leaving the container (not entering a child)
    if (!element.contains(e.relatedTarget)) {
      element.classList.remove('neo-drag-over');
      _removeDropIndicator(element);

      if (typeof options.onDragExit === 'function') {
        var flexEvent = new NeoFlexDragEvent(
          NeoFlexDragEvent.DRAG_EXIT, e, DragManager._dragSource, DragManager._action
        );
        options.onDragExit(flexEvent);
      }
    }
  });

  element.addEventListener('drop', function(e) {
    e.preventDefault();
    element.classList.remove('neo-drag-over');
    _removeDropIndicator(element);

    // Reconstruct DragSource from DataTransfer if needed (cross-component drops)
    var dragSource = DragManager._dragSource;
    if (!dragSource) {
      dragSource = new DragSource();
      var rawData = null;
      try {
        rawData = e.dataTransfer.getData('application/x-openflex-dnd');
      } catch (err) {
        rawData = e.dataTransfer.getData('text/plain');
      }
      if (rawData) {
        try {
          var parsed = JSON.parse(rawData);
          Object.keys(parsed).forEach(function(key) {
            dragSource.addData(parsed[key], key);
          });
        } catch (parseErr) {
          // Could not parse - ignore
        }
      }
    }

    // Calculate insert index
    var selector = options.childSelector || '.neo-list-item, tr.neo-datagrid-row';
    var children = Array.from(element.querySelectorAll(':scope > ' + selector.split(',')[0].trim()));
    if (children.length === 0) {
      children = Array.from(element.children).filter(function(ch) {
        return !ch.classList.contains('neo-drop-indicator');
      });
    }
    var insertIndex = _calcInsertIndex(element, e.clientY, children);

    // Create Flex-style drop event
    var flexEvent = new NeoFlexDragEvent(
      NeoFlexDragEvent.DRAG_DROP, e, dragSource, DragManager._action || 'copy', DragManager._dragInitiator
    );
    flexEvent._insertIndex = insertIndex;

    if (typeof options.onDragDrop === 'function') {
      options.onDragDrop(flexEvent);
    }

    DragManager.endDrag();
  });
}

// ============================================================
// Exports
// ============================================================

var exports = {
  DragSource: DragSource,
  NeoFlexDragEvent: NeoFlexDragEvent,
  DragManager: DragManager,
  setupDragSource: setupDragSource,
  setupDropTarget: setupDropTarget
};

// Node.js / CommonJS
if (typeof module !== 'undefined' && module.exports) {
  module.exports = exports;
}

// Global exports for browser
if (typeof window !== 'undefined') {
  window.OpenFlexDnD = exports;
}
