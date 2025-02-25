import tkinter as tk
import tkinter.ttk as ttk
import random

class DDHelper:
    def __init__(self, root):
        self.root = root
        self.root.title("D&D Helper")
        self.root.geometry("550x600")  # Adjust window size to better fit descriptions

        notebook = ttk.Notebook(root)
        notebook.pack(expand=1, fill='both')

        # Dice Roller Tab
        self.dice_frame = ttk.Frame(notebook)
        notebook.add(self.dice_frame, text='Dice Roller')
        self.create_dice_roller_ui()

        # Attribute Roller Tab
        self.attribute_roller_frame = ttk.Frame(notebook)
        notebook.add(self.attribute_roller_frame, text='Attribute Roller')
        self.create_attribute_roller_ui()

        # Buy Point Generator Tab
        self.buy_point_frame = ttk.Frame(notebook)
        notebook.add(self.buy_point_frame, text='Buy Point Generator')
        self.create_buy_point_generator_ui()

    def create_dice_roller_ui(self):
        # Description
        ttk.Label(self.dice_frame, text="I roll the dice so that you don't have to!").pack(pady=10)

        # Dice Roller UI
        frame = ttk.Frame(self.dice_frame)
        frame.pack(pady=10)

        ttk.Label(frame, text="Type of Die: ").grid(column=0, row=0, padx=5)
        self.die_type = ttk.Combobox(frame, values=['d4', 'd6', 'd8', 'd10', 'd12', 'd20', 'd100'])
        self.die_type.grid(column=1, row=0, padx=5)
        self.die_type.set('d6')

        ttk.Label(frame, text="Number of Dice: ").grid(column=0, row=1, padx=5)
        self.num_dice = ttk.Entry(frame)
        self.num_dice.grid(column=1, row=1, padx=5)
        self.num_dice.insert(0, '1')

        ttk.Label(frame, text="Modifier: ").grid(column=0, row=2, padx=5)
        self.modifier = ttk.Entry(frame)
        self.modifier.grid(column=1, row=2, padx=5)
        self.modifier.insert(0, '0')

        self.roll_result = tk.StringVar()
        ttk.Label(frame, textvariable=self.roll_result, font=('Arial', 24)).grid(column=0, row=4, columnspan=2, pady=10)

        ttk.Button(frame, text="Roll!", command=self.roll_dice).grid(column=0, row=5, columnspan=2, pady=5)

        self.tracked_results = tk.Listbox(frame, height=10, width=40)
        self.tracked_results.grid(column=0, row=6, columnspan=2, pady=10)

        ttk.Button(frame, text="Clear", command=self.clear_results).grid(column=0, row=7, columnspan=2, pady=5)

    def roll_dice(self):
        die = int(self.die_type.get()[1:])  # Extract number from 'dX'
        num = int(self.num_dice.get())
        mod = int(self.modifier.get())

        rolls = [random.randint(1, die) for _ in range(num)]
        total = sum(rolls) + mod
        rolls_str = "+".join(map(str, rolls))
        result = f"{num}d{die} +{mod}: {rolls_str} + {mod} = {total}"
        self.roll_result.set(total)
        self.tracked_results.insert(tk.END, result)

    def clear_results(self):
        self.tracked_results.delete(0, tk.END)
        self.roll_result.set("")

    def create_attribute_roller_ui(self):
        # Description with wrapped text
        description = (
            "Rolls 4d6, discards the lowest, and gives you attribute scores "
            "for you to allocate.\nUse the mulligan threshold to force rerolls "
            "for scores that are lower than you'd like."
        )
        label = ttk.Label(self.attribute_roller_frame, text=description, wraplength=500, justify="center")
        label.pack(pady=10)

        frame = ttk.Frame(self.attribute_roller_frame)
        frame.pack(pady=10)

        ttk.Label(frame, text="Mulligan Threshold: ").grid(column=0, row=0, padx=5)
        self.mulligan_threshold = tk.Entry(frame)
        self.mulligan_threshold.grid(column=1, row=0, padx=5)
        self.mulligan_threshold.insert(0, "10")

        ttk.Button(frame, text="Generate Attributes", command=self.generate_attributes).grid(column=0, row=1, columnspan=2, pady=5)

        self.generated_attributes = tk.Listbox(frame, height=10, width=40)
        self.generated_attributes.grid(column=0, row=2, columnspan=2, pady=10)

    def generate_attributes(self):
        threshold = min(max(int(self.mulligan_threshold.get()), 3), 18)
        while True:
            rolls = [[random.randint(1, 6) for _ in range(4)] for _ in range(6)]
            scores = [sum(sorted(roll)[1:]) for roll in rolls]
            
            if all(score >= threshold for score in scores) and any(score >= 16 for score in scores):
                break

        self.generated_attributes.delete(0, tk.END)
        for score in scores:
            self.generated_attributes.insert(tk.END, score)

    def create_buy_point_generator_ui(self):
        # Description with specific formatting
        description = (
            "Playing something other than DND and decided 'to hell with "
            "min-maxing, let's wing it?'\nThen this tool is for you!"
        )
        label = ttk.Label(self.buy_point_frame, text=description, wraplength=500, justify="center")
        label.pack(pady=10)

        frame = ttk.Frame(self.buy_point_frame)
        frame.pack(pady=10)

        ttk.Label(frame, text="Buy Points: ").grid(column=0, row=0, sticky='E', padx=5, pady=5)
        self.buy_points_entry = ttk.Entry(frame)
        self.buy_points_entry.grid(column=1, row=0, padx=5, pady=5)
        self.buy_points_entry.insert(0, "27")

        ttk.Label(frame, text="Attributes: ").grid(column=0, row=1, sticky='E', padx=5, pady=5)
        self.attribute_count_entry = ttk.Entry(frame)
        self.attribute_count_entry.grid(column=1, row=1, padx=5, pady=5)
        self.attribute_count_entry.insert(0, "6")

        ttk.Label(frame, text="Starting Score: ").grid(column=0, row=2, sticky='E', padx=5, pady=5)
        self.starting_score_entry = ttk.Entry(frame)
        self.starting_score_entry.grid(column=1, row=2, padx=5, pady=5)
        self.starting_score_entry.insert(0, "8")

        ttk.Label(frame, text="Max Score (optional): ").grid(column=0, row=3, sticky='E', padx=5, pady=5)
        self.max_score_entry = ttk.Entry(frame)
        self.max_score_entry.grid(column=1, row=3, padx=5, pady=5)

        # Cost fields
        ttk.Label(frame, text="Point Cost 2 at:").grid(column=0, row=4, sticky='E', padx=5, pady=5)
        self.point_cost_2_entry = ttk.Entry(frame)
        self.point_cost_2_entry.grid(column=1, row=4, padx=5, pady=5)

        ttk.Label(frame, text="Point Cost 3 at:").grid(column=0, row=5, sticky='E', padx=5, pady=5)
        self.point_cost_3_entry = ttk.Entry(frame)
        self.point_cost_3_entry.grid(column=1, row=5, padx=5, pady=5)

        ttk.Label(frame, text="Point Cost 4 at:").grid(column=0, row=6, sticky='E', padx=5, pady=5)
        self.point_cost_4_entry = ttk.Entry(frame)
        self.point_cost_4_entry.grid(column=1, row=6, padx=5, pady=5)

        ttk.Label(frame, text="Point Cost 5 at:").grid(column=0, row=7, sticky='E', padx=5, pady=5)
        self.point_cost_5_entry = ttk.Entry(frame)
        self.point_cost_5_entry.grid(column=1, row=7, padx=5, pady=5)

        self.generate_buy_point_button = ttk.Button(frame, text="Generate", command=self.generate_buy_point_attributes)
        self.generate_buy_point_button.grid(column=0, row=8, columnspan=2, pady=5)

        self.buy_point_result = tk.Text(frame, height=10, width=40)
        self.buy_point_result.grid(column=0, row=9, columnspan=2, padx=5, pady=5)

    def generate_buy_point_attributes(self):
        buy_points = int(self.buy_points_entry.get())
        attribute_count = min(max(int(self.attribute_count_entry.get()), 1), 10)
        starting_score = int(self.starting_score_entry.get())

        try:
            max_score = int(self.max_score_entry.get())
        except ValueError:
            max_score = None

        # Convert the cost thresholds into usable format
        cost_thresholds = {
            2: int(self.point_cost_2_entry.get()) if self.point_cost_2_entry.get() else float('inf'),
            3: int(self.point_cost_3_entry.get()) if self.point_cost_3_entry.get() else float('inf'),
            4: int(self.point_cost_4_entry.get()) if self.point_cost_4_entry.get() else float('inf'),
            5: int(self.point_cost_5_entry.get()) if self.point_cost_5_entry.get() else float('inf'),
        }
        sorted_costs = sorted(cost_thresholds.items(), key=lambda x: x[1])

        attributes = [starting_score] * attribute_count
        remaining_points = buy_points

        def get_cost(current_score):
            cost = 1
            for c, threshold in sorted_costs:
                if current_score >= threshold:
                    cost = c
                else:
                    break
            return cost

        last_index = 0  # Track the last modified index to help with randomness
        # Use all available buy points but also allow skipping some attributes
        attempts = 0
        while remaining_points > 0 and attempts < 100:
            attempts += 1
            for _ in range(attribute_count):
                i = random.randint(0, attribute_count - 1)
                if max_score is not None and attributes[i] >= max_score:
                    continue
                current_cost = get_cost(attributes[i] + 1)
                if remaining_points >= current_cost:
                    attributes[i] += 1
                    remaining_points -= current_cost
                # Early exit if buy points are exhausted
                if remaining_points == 0:
                    break

        self.buy_point_result.delete("1.0", tk.END)
        for i, attr in enumerate(attributes):
            self.buy_point_result.insert(tk.END, f"Attribute {i+1}: {attr}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = DDHelper(root)
    root.mainloop()
