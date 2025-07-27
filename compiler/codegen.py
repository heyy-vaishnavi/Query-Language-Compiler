import pandas as pd

def eval_condition(df, condition):
    if condition is None:
        return df

    cond_type = condition[0]

    if cond_type == 'comparison':
        op = condition[1]
        col = condition[2]
        val = condition[3]

        # ✅ Handle subquery as value
        if isinstance(val, tuple) and val[0] == 'subquery':
            subquery_result = execute_query(val[1])
            if len(subquery_result.columns) != 1 or len(subquery_result) != 1:
                raise ValueError("Subquery must return a single value")
            val = subquery_result.iloc[0, 0]

        if op == '=':
            return df[df[col] == val]
        elif op == '!=':
            return df[df[col] != val]
        elif op == '<':
            return df[df[col] < val]
        elif op == '<=':
            return df[df[col] <= val]
        elif op == '>':
            return df[df[col] > val]
        elif op == '>=':
            return df[df[col] >= val]
        else:
            raise NotImplementedError(f"Operator {op} not supported")

    elif cond_type == 'logic':
        logic_op = condition[1]
        left = condition[2]
        right = condition[3]
        left_df = eval_condition(df, left)
        right_df = eval_condition(df, right)

        if logic_op == 'and':
            return df[left_df.index.intersection(right_df.index)]
        elif logic_op == 'or':
            return df[left_df.index.union(right_df.index)]
        else:
            raise NotImplementedError(f"Logical operator {logic_op} not supported")

    else:
        raise ValueError("Invalid condition type")


def execute_query(parsed_query):
    file_name = parsed_query['file']
    if file_name.endswith('.csv'):
        df = pd.read_csv(file_name)
    elif file_name.endswith('.json'):
        df = pd.read_json(file_name)
    else:
        raise ValueError("Unsupported file format. Only CSV and JSON supported.")

    # Apply WHERE clause first
    where_clause = parsed_query.get('where')
    if where_clause:
        df = eval_condition(df, where_clause)

    columns = parsed_query.get('columns')

    # ⚠️ First handle aggregate functions
    if len(columns) == 1 and isinstance(columns[0], tuple) and columns[0][0] == 'agg':
        func_type, col = columns[0][1], columns[0][2]

        if func_type == 'count' and col == '*':
            return pd.DataFrame({'count': [len(df)]})
        elif func_type == 'count':
            return pd.DataFrame({'count': [df[col].count()]})
        elif func_type == 'sum':
            return pd.DataFrame({'sum': [df[col].sum()]})
        elif func_type == 'avg':
            return pd.DataFrame({'avg': [df[col].mean()]})
        elif func_type == 'min':
            return pd.DataFrame({'min': [df[col].min()]})
        elif func_type == 'max':
            return pd.DataFrame({'max': [df[col].max()]})
        else:
            raise NotImplementedError(f"Aggregate function {func_type} not supported")

    # Apply ORDER BY clause
    orderby = parsed_query.get('orderby')
    if orderby:
        col, direction = orderby if isinstance(orderby, tuple) else (orderby, 'asc')
        df = df.sort_values(by=col, ascending=(direction == 'asc'))


    # Apply LIMIT
    limit = parsed_query.get('limit')
    if limit:
        df = df.head(limit)

    # Select columns
    if columns == ['*']:
        result_df = df
    else:
        result_df = df[columns]

    return result_df.reset_index(drop=True)
