class SortingVisualizer {
    constructor() {
        this.currentArray = [];
        this.currentAlgorithm = 'bubble_sort';
        this.isSorting = false;
        this.isPaused = false;
        this.animationSpeed = 800;
        this.currentStep = 0;
        this.totalSteps = 0;
        this.steps = [];
        this.explanations = [];
        this.logicExplanations = [];
        this.highlights = [];
        this.animationId = null;
        
        this.initializeEventListeners();
        this.generateNewArray();
        this.updateAlgorithmInfo();
    }

    initializeEventListeners() {
        // Algorithm selection
        document.getElementById('algorithm').addEventListener('change', (e) => {
            this.currentAlgorithm = e.target.value;
            this.updateAlgorithmInfo();
        });

        // Array size slider
        const sizeSlider = document.getElementById('arraySize');
        const sizeValue = document.getElementById('sizeValue');
        sizeSlider.addEventListener('input', (e) => {
            sizeValue.textContent = e.target.value;
        });
        sizeSlider.addEventListener('change', () => this.generateNewArray());

        // Speed slider
        const speedSlider = document.getElementById('speed');
        const speedValue = document.getElementById('speedValue');
        speedSlider.addEventListener('input', (e) => {
            this.animationSpeed = parseInt(e.target.value);
            speedValue.textContent = e.target.value;
        });

        // Control buttons
        document.getElementById('generateBtn').addEventListener('click', () => this.generateNewArray());
        document.getElementById('sortBtn').addEventListener('click', () => this.startSorting());
        document.getElementById('pauseBtn').addEventListener('click', () => this.togglePause());
        document.getElementById('resetBtn').addEventListener('click', () => this.resetVisualization());

        // Step navigation
        document.getElementById('prevStepBtn').addEventListener('click', () => this.previousStep());
        document.getElementById('nextStepBtn').addEventListener('click', () => this.nextStep());

        // Test cases
        document.getElementById('bestCaseBtn').addEventListener('click', () => this.loadTestCase('sorted'));
        document.getElementById('worstCaseBtn').addEventListener('click', () => this.loadTestCase('reverse_sorted'));
        document.getElementById('randomCaseBtn').addEventListener('click', () => this.loadTestCase('random'));

        // Tabs
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const tabName = e.target.getAttribute('data-tab');
                this.switchTab(tabName);
            });
        });
    }

    async generateNewArray() {
        const size = parseInt(document.getElementById('arraySize').value);
        const activeCase = document.querySelector('.case-btn.active').classList[1];
        const arrayType = activeCase === 'best' ? 'sorted' : 
                         activeCase === 'worst' ? 'reverse_sorted' : 'random';

        try {
            const response = await fetch('/generate_array', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ size: size, type: arrayType })
            });
            const data = await response.json();
            this.currentArray = data.array;
            this.renderArray(this.currentArray);
            this.resetVisualization();
        } catch (error) {
            console.error('Error generating array:', error);
        }
    }

    async startSorting() {
        if (this.isSorting) return;

        this.isSorting = true;
        this.isPaused = false;
        this.currentStep = 0;
        this.updateControlButtons();

        try {
            const response = await fetch('/sort', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    algorithm: this.currentAlgorithm,
                    array: this.currentArray
                })
            });
            const data = await response.json();
            
            this.steps = data.steps;
            this.explanations = data.explanations;
            this.logicExplanations = data.logic_explanations;
            this.highlights = data.highlights;
            this.totalSteps = data.total_steps;

            this.updateStepCounter();
            this.updateProgressBar();
            this.enableStepNavigation();
            this.startAnimation();
        } catch (error) {
            console.error('Error starting sort:', error);
            this.isSorting = false;
            this.updateControlButtons();
        }
    }

    startAnimation() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }

        const animate = async () => {
            if (this.currentStep < this.totalSteps && this.isSorting && !this.isPaused) {
                this.renderStep(this.currentStep);
                this.currentStep++;
                this.updateStepCounter();
                this.updateProgressBar();
                
                await this.delay(this.animationSpeed);
                this.animationId = requestAnimationFrame(animate);
            } else if (this.currentStep >= this.totalSteps) {
                this.isSorting = false;
                this.updateControlButtons();
                this.showCompletionMessage();
            }
        };

        this.animationId = requestAnimationFrame(animate);
    }

    renderStep(stepIndex) {
        if (stepIndex >= this.totalSteps) return;

        const array = this.steps[stepIndex];
        const highlight = this.highlights[stepIndex];
        const explanation = this.explanations[stepIndex];
        const logicExplanation = this.logicExplanations[stepIndex];

        this.renderArray(array, highlight);
        this.updateExplanations(explanation, logicExplanation);
    }

    renderArray(array, highlight = { comparing: [], swapping: [], sorted: [], pivot: [] }) {
        const container = document.getElementById('arrayVisualization');
        const maxValue = Math.max(...array);
        
        container.innerHTML = '';
        
        array.forEach((value, index) => {
            const bar = document.createElement('div');
            bar.className = 'array-bar';
            bar.style.height = `${(value / maxValue) * 100}%`;
            
            // Add value label
            const label = document.createElement('div');
            label.className = 'bar-label';
            label.textContent = value;
            bar.appendChild(label);

            // Apply highlighting
            if (highlight.pivot.includes(index)) {
                bar.classList.add('pivot');
            } else if (highlight.sorted.includes(index)) {
                bar.classList.add('sorted');
            } else if (highlight.swapping.includes(index)) {
                bar.classList.add('swapping');
            } else if (highlight.comparing.includes(index)) {
                bar.classList.add('comparing');
            } else {
                bar.classList.add('unsorted');
            }

            container.appendChild(bar);
        });
    }

    updateExplanations(stepExplanation, logicExplanation) {
        document.getElementById('stepExplanation').textContent = stepExplanation;
        document.getElementById('logicExplanation').textContent = logicExplanation;
    }

    updateStepCounter() {
        document.getElementById('stepCounter').textContent = 
            `Step: ${this.currentStep}/${this.totalSteps}`;
    }

    updateProgressBar() {
        const progress = this.totalSteps > 0 ? (this.currentStep / this.totalSteps) * 100 : 0;
        document.getElementById('progressFill').style.width = `${progress}%`;
    }

    togglePause() {
        this.isPaused = !this.isPaused;
        const pauseBtn = document.getElementById('pauseBtn');
        
        if (this.isPaused) {
            pauseBtn.innerHTML = '<i class="fas fa-play"></i> Resume';
            pauseBtn.classList.remove('btn-warning');
            pauseBtn.classList.add('btn-success');
        } else {
            pauseBtn.innerHTML = '<i class="fas fa-pause"></i> Pause';
            pauseBtn.classList.remove('btn-success');
            pauseBtn.classList.add('btn-warning');
            this.startAnimation();
        }
    }

    resetVisualization() {
        this.isSorting = false;
        this.isPaused = false;
        this.currentStep = 0;
        
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }
        
        this.steps = [];
        this.explanations = [];
        this.logicExplanations = [];
        this.highlights = [];
        
        this.renderArray(this.currentArray);
        this.updateControlButtons();
        this.updateStepCounter();
        this.updateProgressBar();
        this.disableStepNavigation();
        
        document.getElementById('stepExplanation').textContent = 
            'Select an algorithm and click Start to begin visualization.';
        document.getElementById('logicExplanation').textContent = 
            'Detailed algorithm logic will appear here during visualization.';
    }

    previousStep() {
        if (this.currentStep > 0) {
            this.currentStep--;
            this.renderStep(this.currentStep);
            this.updateStepCounter();
            this.updateProgressBar();
            this.updateStepNavigation();
        }
    }

    nextStep() {
        if (this.currentStep < this.totalSteps - 1) {
            this.currentStep++;
            this.renderStep(this.currentStep);
            this.updateStepCounter();
            this.updateProgressBar();
            this.updateStepNavigation();
        }
    }

    enableStepNavigation() {
        document.getElementById('prevStepBtn').disabled = false;
        document.getElementById('nextStepBtn').disabled = false;
    }

    disableStepNavigation() {
        document.getElementById('prevStepBtn').disabled = true;
        document.getElementById('nextStepBtn').disabled = true;
    }

    updateStepNavigation() {
        document.getElementById('prevStepBtn').disabled = this.currentStep <= 0;
        document.getElementById('nextStepBtn').disabled = this.currentStep >= this.totalSteps - 1;
    }

    updateControlButtons() {
        const isActive = this.isSorting;
        document.getElementById('sortBtn').disabled = isActive;
        document.getElementById('pauseBtn').disabled = !isActive;
        document.getElementById('resetBtn').disabled = !isActive;
        document.getElementById('generateBtn').disabled = isActive;
        document.getElementById('algorithm').disabled = isActive;
        document.getElementById('arraySize').disabled = isActive;
        
        const pauseBtn = document.getElementById('pauseBtn');
        if (!isActive) {
            pauseBtn.innerHTML = '<i class="fas fa-pause"></i> Pause';
            pauseBtn.classList.remove('btn-success');
            pauseBtn.classList.add('btn-warning');
        }
    }

    async loadTestCase(type) {
        // Update active case button
        document.querySelectorAll('.case-btn').forEach(btn => btn.classList.remove('active'));
        if (type === 'sorted') {
            document.getElementById('bestCaseBtn').classList.add('active');
        } else if (type === 'reverse_sorted') {
            document.getElementById('worstCaseBtn').classList.add('active');
        } else {
            document.getElementById('randomCaseBtn').classList.add('active');
        }
        
        await this.generateNewArray();
    }

    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
        
        // Update tab content
        document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));
        document.getElementById(tabName + 'Tab').classList.add('active');
    }

    updateAlgorithmInfo() {
        const algorithm = this.currentAlgorithm;
        const info = {
            'bubble_sort': {
                name: 'Bubble Sort',
                best: 'O(n) - When array is already sorted',
                worst: 'O(n²) - When array is reverse sorted',
                desc: 'Repeatedly compares adjacent elements and swaps them if they are in wrong order.'
            },
            'selection_sort': {
                name: 'Selection Sort',
                best: 'O(n²)',
                worst: 'O(n²)',
                desc: 'Finds minimum element and places it at the beginning repeatedly.'
            },
            'insertion_sort': {
                name: 'Insertion Sort',
                best: 'O(n) - When array is already sorted',
                worst: 'O(n²) - When array is reverse sorted',
                desc: 'Builds sorted array one item at a time by inserting elements in correct position.'
            },
            'merge_sort': {
                name: 'Merge Sort',
                best: 'O(n log n)',
                worst: 'O(n log n)',
                desc: 'Divides array into halves, sorts them, and merges the sorted halves.'
            },
            'quick_sort': {
                name: 'Quick Sort',
                best: 'O(n log n)',
                worst: 'O(n²) - When pivot is always smallest/largest',
                desc: 'Picks pivot element and partitions array around the pivot.'
            }
        }[algorithm];

        document.getElementById('algorithmInfo').innerHTML = `
            <p><strong>Algorithm:</strong> ${info.name}</p>
            <p><strong>Best Case:</strong> ${info.best}</p>
            <p><strong>Worst Case:</strong> ${info.worst}</p>
            <p><strong>Description:</strong> ${info.desc}</p>
        `;
    }

    showCompletionMessage() {
        document.getElementById('stepExplanation').textContent = 
            '🎉 Sorting completed! The array is now fully sorted.';
        document.getElementById('logicExplanation').textContent = 
            'The algorithm has successfully sorted the array. You can review the steps using the navigation buttons.';
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Initialize the visualizer when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new SortingVisualizer();
});