function updateCustomPaginator(idTable, paginationId) {
    if (paginationId) {
        const gridApi = gridInstances[idTable];

        if (!gridApi) {
            console.error('Error: AG Grid API no disponible para la tabla:', idTable);
            return;
        }
        const currentPage = gridApi.paginationGetCurrentPage() + 1;
        const totalPages = gridApi.paginationGetTotalPages();

        document.getElementById(`page_info_${paginationId}`).textContent = `Pág ${currentPage} de ${totalPages}`;

        const prevButton = document.getElementById(`paginate_previous_${paginationId}`);
        const nextButton = document.getElementById(`paginate_next_${paginationId}`);

        if (currentPage === 1) {
            prevButton.classList.add('disabled');
        } else {
            prevButton.classList.remove('disabled');
        }

        if (currentPage === totalPages || totalPages === 0) {
            nextButton.classList.add('disabled');
        } else {
            nextButton.classList.remove('disabled');
        }
    }
}


function drawTableGridGeneral(data, idTable, headers, paginationPage, posicion, paginationId, heightRow,idSpinner) {

    if (!Array.isArray(data) || data.length == 0) {
        setTimeout(() => {
            hideSpinnerByCard(idSpinner);
        }, 1000);
        return;
    }
    const gridElement = document.getElementById(idTable);
    if (gridElement) {
        if (gridInstances[idTable] && gridInstances[idTable].api) {
            gridInstances[idTable].api.destroy();
        }
        gridElement.innerHTML = '';
    }
    const customIcons = {
        sortAscending: `<span class="ag-icon ag-icon-asc" unselectable="on" role="presentation"></span>`,
        sortDescending: `<span class="ag-icon ag-icon-desc" unselectable="on" role="presentation"></span>`,
        sortNone: `<span class="ag-icon ag-icon-none" unselectable="on" role="presentation"></span>`,
        filter: `<span class="ag-icon ag-icon-filter" unselectable="on" role="presentation"></span>`
    };
    if (posicion) {
        if (Array.isArray(data)) {
            data.forEach((obj, index) => {
                obj.index = index + 1;
            });
        }
    }
    let columnDefs = [];
    let multiplicadorFlex;
    const keys = Object.keys(headers);
    if (headers[keys[keys.length - 1]].flex != null && headers[keys[keys.length - 1]].flex < 1) {
        const flex = headers[keys[keys.length - 1]].flex
        multiplicadorFlex = 1 / (flex > 0 ? flex : 1)
    } else {
        multiplicadorFlex = 1
    }
    for (let i = 0; i < keys.length; i++) {
        let key = keys[i];
        if (headers.hasOwnProperty(key)) {

            let headerClass = headers[key].headerClass;
            let cellClass = headers[key].cellClass;
            let finalHeaderClass = 'custom-header';
            let finalCellclass = 'custom-cell-class';

            if (headerClass) {
                if (Array.isArray(headerClass)) {
                    finalHeaderClass = ['custom-header', ...headerClass].join(' ');
                } else {
                    finalHeaderClass = headerClass;
                }
            }
            if (cellClass) {
                if (Array.isArray(cellClass)) {
                    finalCellclass = ['custom-cell-class', ...cellClass].join(' ');
                } else {
                    finalCellclass = cellClass;
                }
            }
            let encabezado = {
                headerName: headers[key].title,
                field: key,
                suppressMovable: true,
                headerClass: finalHeaderClass,
                flex: (headers[key].flex != null ? headers[key].flex : 1) * multiplicadorFlex,
                sort: null,
                unSortIcon: true,
                lockPosition: true,
                cellClass: finalCellclass,
            };
            encabezado.sortable = headers[key].sortable !== false;
            encabezado.minWidth =  headers[key].minWidth || 150;

            if (headers[key].resizable != null) {
                encabezado.resizable = headers[key].resizable
            } else {
                encabezado.resizable = i === keys.length - 1 ? false : true
            }
            if (data.length <= 1) {
                encabezado.sortable = false
            }
            // Corregir el nombre de 'cellRender' a 'cellRenderer'
            if (headers[key].valueFormatter) encabezado.valueFormatter = headers[key].valueFormatter;
            if (headers[key].cellRenderer) encabezado.cellRenderer = headers[key].cellRenderer; // Cambié 'cellRender' a 'cellRenderer'

            columnDefs.push(encabezado);
        }
    }
    if (Array.isArray(data)) {
        const gridOptions = {
            theme: "legacy",
            columnDefs: columnDefs,
            rowData: data,
            pagination: false,
            suppressHorizontalScroll: false,
            suppressPaginationPanel: true,
            suppressCellFocus: true,
            domLayout: 'autoHeight',
            rowStyle: { fontFamily: 'Roboto', fontSize: '20px' },
            getRowHeight: function (params) {
                const lineHeight = 5; // Altura de una línea en píxeles -> Se modificó de 18 a 10
                const padding = 8; // Espacio adicional para padding
                let maxLines = 1; // Mínimo una línea por defecto
                // Obtener el ancho de las columnas
                const columnDefs = params.api.getColumnDefs(); // Obtener las definiciones de las columnas
                const columnWidths = {};
                columnDefs.forEach(col => {
                    columnWidths[col.field] = col.width || col.minWidth || 150; // Usar el ancho definido o un valor por defecto
                });
                // Calcular el número de líneas para cada celda
                Object.keys(params.data).forEach(key => {
                    const cellContent = params.data[key];
                    if (typeof cellContent === 'string' && !cellContent.includes('<img')) {
                        // Obtener el ancho de la columna actual
                        const columnWidth = columnWidths[key];
                        const charsPerLine = Math.floor(columnWidth / 20); // Aproximación de caracteres por línea (24px por caracter)
                        const cellLines = Math.ceil(cellContent.length / charsPerLine);
                        maxLines = Math.max(maxLines, cellLines);
                    }
                });
                // Calcular la altura de la fila
                let rowHeight = maxLines * lineHeight + padding;
                if (isNaN(rowHeight)) {
                    rowHeight = 1
                }
                // Si se proporciona una altura fija (heightRow), usarla; de lo contrario, usar la altura calculada
                return heightRow == null || rowHeight < heightRow ? heightRow : rowHeight;
            },
            onColumnResized: (params) => {
                params.api.resetRowHeights(); // Recalcula la altura de las filas
            },
            onGridReady: function(params) {
                const gridApi = params.api;
                gridInstances[idTable] = params.api;
            },
            onPaginationChanged: function () {
                setTimeout(() => {
                    updateCustomPaginator(idTable, paginationId);
                }, 100);
            }
        };
        if (paginationId) {
            let paginationP = paginationPage || 10
            gridOptions.pagination = true; // Habilitar la paginación
            gridOptions.paginationPageSize = paginationP; // Asignar el nuevo valor para el tamaño de página
            gridOptions.paginationPageSizeSelector = [paginationP, 7, 14, 30]; // Asignar las opciones para el selector de tamaño de página
        }
        const gridDiv = document.querySelector('#' + idTable);
        gridInstances[idTable] = agGrid.createGrid(gridDiv, gridOptions);
        let element = document.getElementById(idTable);
        element.style.setProperty('position', 'relative');
        element.style.setProperty('padding', '3px 0px 0px 0px');
        element.style.setProperty('width', '100%');
        if (paginationId) {
            const paginationContainer = document.createElement('div');
            paginationContainer.classList.add('dataTables_paginate', 'paging_simple', 'text-center');
            paginationContainer.style.cssText += 'margin: 10px 0 10px !important;'
            paginationContainer.id = paginationId;
            paginationContainer.style.display = 'flex';
            paginationContainer.style.justifyContent = 'end';
            paginationContainer.style.alignItems = 'center';
            paginationContainer.style.gap = '10px';
            paginationContainer.style.padding = '0 15px';
    
            const prevButton = document.createElement('div');
            prevButton.classList.add('paginate_button', 'previous', 'disabled');
            prevButton.id = `paginate_previous_${paginationId}`;
            prevButton.style.width = '32px';
            prevButton.style.height = '32px';
            prevButton.style.background = 'rgb(104, 104, 104)';
            prevButton.style.borderRadius = '6px';
            prevButton.style.display = 'flex';
            prevButton.style.alignItems = 'center';
            prevButton.style.justifyContent = 'center';
            prevButton.style.cursor = 'pointer';
            prevButton.innerHTML = `<i class="bi bi-arrow-left-short" style="font-size: 28px; color: #fff;"></i>`;
            prevButton.addEventListener('click', () => {
                gridInstances[idTable].paginationGoToPreviousPage();
            });
            const pageInfo = document.createElement('span');
            pageInfo.classList.add('datatable-info-text');
            pageInfo.id = `page_info_${paginationId}`;
            pageInfo.style.color = '#9C9B9B';
            pageInfo.style.fontSize = '12px';
            pageInfo.style.fontFamily = 'Poppins';
            pageInfo.style.fontWeight = '700';
            pageInfo.style.lineHeight = '16px';
            pageInfo.textContent = `Pág 1 de 6`;
            const nextButton = document.createElement('div');
            nextButton.classList.add('paginate_button', 'next');
            nextButton.id = `paginate_next_${paginationId}`;
            nextButton.style.width = '32px';
            nextButton.style.height = '32px';
            nextButton.style.background = 'rgb(104, 104, 104)';
            nextButton.style.borderRadius = '6px';
            nextButton.style.display = 'flex';
            nextButton.style.alignItems = 'center';
            nextButton.style.justifyContent = 'center';
            nextButton.style.cursor = 'pointer';
            nextButton.innerHTML = `<i class="bi bi-arrow-right-short" style="font-size: 28px; color: #fff;"></i>`;
            nextButton.addEventListener('click', () => {
                gridInstances[idTable].paginationGoToNextPage();
            });
            paginationContainer.appendChild(prevButton);
            paginationContainer.appendChild(pageInfo);
            paginationContainer.appendChild(nextButton);
            const paginationDivContainer = document.createElement('div');
            paginationDivContainer.style.position = 'relative';
            paginationDivContainer.style.width = '100%';
            paginationDivContainer.style.boxSizing = 'border-box';
            gridElement.appendChild(paginationDivContainer);
            paginationDivContainer.appendChild(paginationContainer);
        }
        const gridContainer = document.querySelector(`#${idTable} .ag-center-cols-container`);
        const gridHeader = document.querySelector(`#${idTable} .ag-header`);

        const Header = gridHeader.style.height.replace('px', '')
        const autoHeightLayuot  =document.querySelector(`#${idTable} .ag-layout-auto-height`);
        let tamanoTabla
        if (data.length > 10){
            tamanoTabla = heightRow ? heightRow * 10 : 400
        }else{
            tamanoTabla = heightRow ? heightRow * data.lenght : 400
        }

        if (gridContainer) {
            element.style.setProperty('height', `${tamanoTabla + parseInt(Header)}px `)
            gridContainer.style.maxHeight = `${tamanoTabla}px`; // Ajusta la altura según sea necesario
            gridContainer.style.overflowY = 'auto';  // Habilita el scroll vertical
            gridContainer.style.overflowX = 'hidden'
        }
        gridDiv.querySelector('.ag-header').style.setProperty('margin-top', '0px', 'important');

    } else {
        console.error("El 'data' recibido no es un array válido.");
    }
    setTimeout(() => {
        hideSpinnerByCard(idSpinner);
    }, 1000);
}