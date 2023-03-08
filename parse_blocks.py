with open('Blocks.txt', 'r', encoding='utf-8') as file:

    char_ranges = {}

    for line in file:

        if line.startswith('#') or line.strip() == '':
            continue

        fields = line.strip().split(';')

        block_name = fields[1].strip()
        char_range = fields[0].strip().split('..')

        char_ranges[block_name] = (int(char_range[0], 16), int(char_range[1], 16))

print(char_ranges)
