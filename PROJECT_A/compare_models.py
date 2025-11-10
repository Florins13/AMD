import matplotlib.pyplot as plt
import numpy as np
from classifier_models import OrangeClassifierManager


def compare_all_models(dataset_name="dataset.tab", split_ratio=0.8):
    """
    Compare hit rates (accuracy) of all classifier models and display in a graph.
    """
    print("=" * 60)
    print("MODEL COMPARISON - HIT RATE ANALYSIS")
    print("=" * 60)
    
    # Initialize the classifier manager
    manager = OrangeClassifierManager(dataset_name, split_ratio)
    
    # Train all models and get error rates
    print("\nTraining all models...")
    classifiers, error_rates = manager.train_all_models()
    
    # Convert error rates to hit rates (accuracy)
    model_names = ['One Rule', 'Decision Tree', 'Naive Bayes']
    model_keys = ['one_rule', 'tree', 'naive_bayes']
    
    hit_rates = []
    for key in model_keys:
        error_rate = error_rates[key]
        hit_rate = (1 - error_rate) * 100  # Convert to percentage
        hit_rates.append(hit_rate)
    
    # Display results
    print("\n" + "=" * 60)
    print("RESULTS:")
    print("=" * 60)
    for i, name in enumerate(model_names):
        print(f"{name:20s}: {hit_rates[i]:6.2f}% accuracy (Error: {error_rates[model_keys[i]]*100:.2f}%)")
    print("=" * 60)
    
    # Create bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create bars
    x_pos = np.arange(len(model_names))
    bars = ax.bar(x_pos, hit_rates, color=['#FF6B6B', '#4ECDC4', '#45B7D1'], 
                   alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Customize the chart
    ax.set_xlabel('Classifier Models', fontsize=12, fontweight='bold')
    ax.set_ylabel('Hit Rate (Accuracy %)', fontsize=12, fontweight='bold')
    ax.set_title(f'Classifier Models Comparison - Hit Rate\nDataset: {dataset_name}', 
                 fontsize=14, fontweight='bold')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(model_names, fontsize=11)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels on top of bars
    for i, (bar, hit_rate) in enumerate(zip(bars, hit_rates)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{hit_rate:.2f}%',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # Add a horizontal line at 50% for reference
    ax.axhline(y=50, color='red', linestyle='--', alpha=0.5, label='50% baseline')
    ax.legend()
    
    plt.tight_layout()
    
    # Save the plot
    output_file = 'model_comparison_hit_rate.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nGraph saved as: {output_file}")
    
    # Display the plot
    plt.show()
    
    return model_names, hit_rates, error_rates


def compare_multiple_runs(dataset_name, num_runs=10, split_ratio=0.8):
    """
    Run the comparison multiple times with different train/test splits
    and show average hit rates with error bars.
    """
    print("=" * 60)
    print(f"MULTIPLE RUNS COMPARISON ({num_runs} runs)")
    print("=" * 60)
    
    model_keys = ['one_rule', 'tree', 'naive_bayes']
    model_names = ['One Rule', 'Decision Tree', 'Naive Bayes']
    
    all_hit_rates = {key: [] for key in model_keys}
    
    for run in range(num_runs):
        print(f"\nRun {run + 1}/{num_runs}...")
        manager = OrangeClassifierManager(dataset_name, split_ratio)
        classifiers, error_rates = manager.train_all_models()
        
        for key in model_keys:
            hit_rate = (1 - error_rates[key]) * 100
            all_hit_rates[key].append(hit_rate)
    
    # Calculate statistics
    means = [np.mean(all_hit_rates[key]) for key in model_keys]
    stds = [np.std(all_hit_rates[key]) for key in model_keys]
    
    print("\n" + "=" * 60)
    print("AVERAGE RESULTS OVER", num_runs, "RUNS:")
    print("=" * 60)
    for i, name in enumerate(model_names):
        print(f"{name:20s}: {means[i]:6.2f}% ± {stds[i]:5.2f}%")
    print("=" * 60)
    
    # Create bar chart with error bars
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x_pos = np.arange(len(model_names))
    bars = ax.bar(x_pos, means, yerr=stds, capsize=10,
                   color=['#FF6B6B', '#4ECDC4', '#45B7D1'], 
                   alpha=0.8, edgecolor='black', linewidth=1.5,
                   error_kw={'linewidth': 2, 'ecolor': 'black'})
    
    # Customize the chart
    ax.set_xlabel('Classifier Models', fontsize=12, fontweight='bold')
    ax.set_ylabel('Hit Rate (Accuracy %)', fontsize=12, fontweight='bold')
    ax.set_title(f'Classifier Models Comparison - Average Hit Rate ({num_runs} runs)\nDataset: {dataset_name}', 
                 fontsize=14, fontweight='bold')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(model_names, fontsize=11)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels
    for i, (bar, mean, std) in enumerate(zip(bars, means, stds)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + std + 2,
                f'{mean:.1f}%',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    
    # Save the plot
    output_file = 'model_comparison_multiple_runs.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nGraph saved as: {output_file}")
    
    plt.show()
    
    return model_names, means, stds


if __name__ == "__main__":
    import sys
    
    # Default values
    dataset_name = "dataset.tab"
    
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == '--multiple':
        # Run multiple times for more robust comparison
        num_runs = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        # Check if dataset is specified
        if len(sys.argv) > 3:
            dataset_name = sys.argv[3]
        compare_multiple_runs(dataset_name=dataset_name, num_runs=num_runs)
    else:
        # Single run comparison
        # Check if dataset is specified as first argument
        if len(sys.argv) > 1:
            dataset_name = sys.argv[1]
        compare_all_models(dataset_name=dataset_name)
