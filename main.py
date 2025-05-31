from typing import List, Dict, Any
import argparse


def read_csv_data(filepath: str) -> List[Dict[str, str]]:
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = [line.strip().split(',') for line in file]
        headers = lines[0]
        return [dict(zip(headers, row)) for row in lines[1:]]


def process_employee_data(entries: List[Dict[str, str]]) -> Dict[str, List[Dict[str, Any]]]:
    grouped_data: Dict[str, List[Dict[str, Any]]] = {}
    for entry in entries:
        department = entry.get('department', 'No Department')
        hours_worked = float(entry.get('hours', '0'))
        rate_key = next((key for key in ['hourly_rate', 'rate', 'salary'] if key in entry), None)
        hourly_rate = float(entry.get(rate_key, '0')) if rate_key else 0.0
        total_pay = hours_worked * hourly_rate
        employee_info = {
            'employee_name': entry.get('name', 'Unnamed'),
            'hours_worked': hours_worked,
            'hourly_rate': hourly_rate,
            'total_pay': total_pay
        }
        if department not in grouped_data:
            grouped_data[department] = []
        grouped_data[department].append(employee_info)
    return grouped_data


def payout_report(all_data: List[List[Dict[str, str]]]) -> str:
    combined_data: Dict[str, List[Dict[str, Any]]] = {}
    for dataset in all_data:
        grouped = process_employee_data(dataset)
        for dept, employees in grouped.items():
            if dept not in combined_data:
                combined_data[dept] = []
            combined_data[dept].extend(employees)
    result = []
    for dept, employees in combined_data.items():
        result.append(f"{dept}")
        result.append("-" * len(dept))
        result.append(f"{'name':<20} {'hours':>6} {'rate':>6} {'payout':>8}")
        for i in employees:
            result.append(
                f"{i['employee_name']:<20} "
                f"{i['hours_worked']:>6.0f} "
                f"{i['hourly_rate']:>6.0f} "
                f"${i['total_pay']:>6.0f}"
            )
        hours = sum(i['hours_worked'] for i in employees)
        payout = sum(i['total_pay'] for i in employees)
        result.append("-" * 20)
        result.append(f"{'':<20} {hours:>6.0f} {'':>6} ${payout:>6.0f}")
        result.append("")
    return "\n".join(result).strip()


def run_report(args: argparse.Namespace) -> None:
    if args.report != 'payout':
        print("Error: Недопустимый тип репорта.")
        return
    datasets = [read_csv_data(file) for file in args.files]
    output = payout_report(datasets)
    print(output)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+')
    parser.add_argument('--report', default='payout')
    return parser.parse_args()

if __name__ == "__main__":
    arguments = main()
    run_report(arguments)