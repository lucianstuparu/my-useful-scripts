import re
import sys
import argparse

def parse_config(config_path):
    variables = {}
    with open(config_path, 'r') as f:
        for line in f:
            # Remove comments and whitespace
            line = line.split('#', 1)[0].strip()
            if not line:
                continue
            if '=' not in line:
                print(f"Skipping invalid line: {line}")
                continue
            name, value = line.split('=', 1)
            name = name.strip()
            value = value.strip()
            variables[name] = value
    return variables

def replace_variables(input_path, output_path, variables):
    with open(input_path, 'r') as f:
        content = f.read()

    # Replace all occurrences of each variable in the format {{name}}
    for name, value in variables.items():
        # Using f-strings to construct the regex pattern
        pattern = rf'\{{\{{\s*{re.escape(name)}\s*\}}\}}'
        content = re.sub(pattern, value, content)

    with open(output_path, 'w') as f:
        f.write(content)

def main():
    parser = argparse.ArgumentParser(description='Replace variables in a text file based on a config file.')
    parser.add_argument('config', help='Path to the config file')
    parser.add_argument('input', help='Path to the input text file')
    parser.add_argument('output', help='Path to the output text file')
    args = parser.parse_args()

    variables = parse_config(args.config)
    replace_variables(args.input, args.output, variables)
    print(f"Replacements done. Output saved to {args.output}")

if __name__ == '__main__':
    main()
