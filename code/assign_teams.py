import pandas as pd
from pathlib import Path


def load_students(students_path: Path, excel_path: Path) -> pd.DataFrame:
    students = pd.read_csv(students_path)
    excel_df = pd.read_excel(excel_path)

    name_col = "NAME OF THE STUDENT"
    prog_col = [c for c in excel_df.columns if "Programme" in str(c)][0]

    excel_trimmed = excel_df[[name_col, prog_col]].copy()
    excel_trimmed.rename(columns={name_col: "student_name", prog_col: "programme"}, inplace=True)

    # Drop any existing programme / programme_group columns to avoid duplicates
    for col in ["programme", "programme_group"]:
        if col in students.columns:
            students = students.drop(columns=[col])

    merged = students.merge(excel_trimmed, on="student_name", how="left")
    return merged


def programme_group(prog: str) -> str:
    if not isinstance(prog, str):
        return "Unknown"
    prog = prog.strip()
    comp = {
        "B Tech Computer",
        "MBA Tech Computer",
        "B Tech IT",
        "MBA Tech IT",
        "B Tech Data Science",
    }
    aia = {
        "B Tech AI",
        "MBA Tech AI",
        "B Tech Cyber Security",
    }
    other = {
        "B Tech EXTC",
        "B Tech Mechanical",
    }
    if prog in comp:
        return "CompGroup"
    if prog in aia:
        return "AIAGroup"
    if prog in other:
        return "OtherGroup"
    return "OtherGroup"


def assign_teams(
    df: pd.DataFrame,
    team_size: int = 4,
    target_cross_teams: int | None = None,
    seed: int = 42,
) -> pd.DataFrame:
    """Assign teams with a specified number of cross-disciplinary teams.

    - First, explicitly form `target_cross_teams` teams that mix programme_groups.
    - Remaining students are packed into same-group teams where possible.
    """

    df = df.copy()
    df["programme_group"] = df["programme"].apply(programme_group)

    # Shuffle deterministically
    df = df.sample(frac=1.0, random_state=seed).reset_index(drop=True)

    df["team_id"] = ""
    df["condition"] = ""

    teams: list[tuple[list[int], str]] = []

    # If no target specified, default to roughly half cross teams
    if target_cross_teams is None:
        total_students = len(df)
        total_teams = total_students // team_size
        target_cross_teams = max(1, total_teams // 2)

    # --- Step 1: form cross teams ---
    remaining_indices = list(df.index)
    rng = pd.Series(remaining_indices).sample(frac=1.0, random_state=seed + 1).tolist()

    def can_form_cross(candidate_indices: list[int]) -> bool:
        groups = {df.loc[i, "programme_group"] for i in candidate_indices}
        return len(groups) > 1

    formed_cross = 0
    used_indices: set[int] = set()

    # Greedy: keep trying to form cross teams until target met or not enough students
    i = 0
    while formed_cross < target_cross_teams and i + team_size <= len(rng):
        candidate = rng[i : i + team_size]
        if any(idx in used_indices for idx in candidate):
            i += team_size
            continue
        if can_form_cross(candidate):
            teams.append((candidate, "cross"))
            used_indices.update(candidate)
            formed_cross += 1
        i += team_size

    # --- Step 2: form same-group teams from remaining students ---
    remaining_indices = [idx for idx in df.index if idx not in used_indices]
    remaining_df = df.loc[remaining_indices].copy()

    for group_name, group_df in remaining_df.groupby("programme_group"):
        idxs = list(group_df.index)
        while len(idxs) >= team_size:
            team_idxs = idxs[:team_size]
            idxs = idxs[team_size:]
            teams.append((team_idxs, "same"))
        # any leftovers are kept aside
        remaining_indices = [idx for idx in remaining_indices if idx not in group_df.index or idx in idxs]

    # --- Step 3: handle any leftover students (pack into last teams) ---
    leftovers = [idx for idx in df.index if idx not in {i for indices, _ in teams for i in indices}]
    if leftovers:
        # Add leftovers to existing teams one-by-one to keep sizes 4±1
        t_idx = 0
        for idx in leftovers:
            teams[t_idx % len(teams)][0].append(idx)
            t_idx += 1

    # Assign team IDs and conditions
    team_counter = 1
    for indices, cond in teams:
        team_label = f"T{team_counter:02d}"
        df.loc[indices, "team_id"] = team_label
        df.loc[indices, "condition"] = cond
        team_counter += 1

    return df


def main() -> None:
    base_dir = Path(__file__).resolve().parents[1]
    students_path = base_dir / "data" / "students.csv"
    excel_path = base_dir / "Current list of students OE.xlsx"

    df = load_students(students_path, excel_path)
    df_with_teams = assign_teams(df, team_size=4, target_cross_teams=7, seed=42)

    # Move programme column next to branch if present
    cols = list(df_with_teams.columns)
    for col in ["programme_group"]:
        if col not in cols:
            continue
    df_with_teams.to_csv(students_path, index=False)

    # Print summary
    print("Total students:", len(df_with_teams))
    print("Teams formed:")
    print(df_with_teams.groupby(["team_id", "condition"])["student_id"].count())


if __name__ == "__main__":
    main()
