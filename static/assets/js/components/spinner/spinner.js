
/**
 * This function shows only one spinner by id
 *
 * @param {*} id  componente HTML
 */
function showSpinnerOnly(id) {

    const spinner = document.getElementById('spinner-' + id);
    const card = document.getElementById(id);
    const BarChartCard = document.getElementById('dias_chart_container')
    const TrendChartCard = document.getElementById('outer-container')

    /* Verificar si los elementos existen */
    if (spinner) {
        spinner.classList.remove('hidden')
    } else {
        console.warn(`Spinner con id 'spinner-${id}' no encontrado.`);
    }

    if (card) {
        card.classList.add('dimmed');
        if (spinner) {
            try {
                let height = card.getAttribute('height');
                spinner.style.height = `${height}px`
                spinner.style.minHeight = '450px'
            } catch {
                console.log('no se encontro height')
            }
        }
    }

    if (BarChartCard) {
        BarChartCard.style.overflowX = 'hidden';
    }

    if (TrendChartCard) {
        TrendChartCard.setAttribute('style', 'overflow-x: hidden;');
    }

}

/** This function drwas all spinners on components selected inside */
function spinnerDraw() {

    showSpinnerOnly('mapid');
    showSpinnerOnly('mapa_tabla');

    showSpinnerOnly('myTreemapEntidades');
    showSpinnerOnly('entidades_table');

    showSpinnerOnly('myBarChart');
    showSpinnerOnly('contratistas_table');
    showSpinnerOnly('myDoughnutChart');

    showSpinnerOnly('myBarChartHorizontal');
    showSpinnerOnly('datatable-adjudicaciones');

    showSpinnerOnly('LineChart');
    showSpinnerOnly('tablesAE');
    showSpinnerOnly('BarChartIpc');
    showSpinnerOnly('tabla-ipc');
}


/**
 * This function hide spinner on a single element by html id
 *
 * @param {*} id de componente HTML
 */
function hideSpinnerOnly(id) {
    const spinner = document.getElementById('spinner-' + id);
    const BarChartCard = document.getElementById('dias_chart_container')
    const TrendChartCard = document.getElementById('outer-container')
    
    if (spinner) {
        spinner.classList.add('hidden');
    } else {
        console.log('spinner NOT found!', spinner)
    }


    if (BarChartCard) {
        BarChartCard.style.overflowX = 'auto';
    }
    if (TrendChartCard) {
        TrendChartCard.setAttribute('style', 'overflow-x: auto;');
    }
}


/**
 * This function creates and appends a spinner overlay to a specified HTML card element.
 * The overlay includes a spinner animation and a loading text.
 *
 * @param {string} cardId - The id of the HTML card element to which the spinner overlay will be appended.
 *
 * @returns {void}
 */
function showSpinnerOnlyByCard(cardId) {
    const card = document.getElementById(cardId);

    if (!card) return;
    const overlay = document.createElement("div");
    overlay.classList.add("spinner-overlay");
    overlay.id = `overlay-${cardId}`;
    const spinner = document.createElement("div");
    spinner.classList.add("spinner-border");
    spinner.classList.add("spinnerCard");
    spinner.id = `spinner-${cardId}`;

    const loadingText = document.createElement("p");
    loadingText.classList.add("loading-text-info");
    loadingText.textContent = "Cargando";
    if (card) {
        overlay.appendChild(spinner);
        overlay.appendChild(loadingText);
        card.appendChild(overlay);
    }
}




function hideSpinnerByCard(cardId) {
    const spinner = document.getElementById(`overlay-${cardId}`);
    if (spinner) {
        spinner.remove();
    }
}

function spinnerDrawByCards (cardIds){
    cardIds.forEach(cardId => {
        showSpinnerOnlyByCard(cardId);
    });

}