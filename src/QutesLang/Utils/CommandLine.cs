using System.CommandLine;

namespace QutesLang.Utils;

public class CommandLine
{
    public static Option<T> CreateOption<T>(string[] aliases, Func<T> defaultValueFactory, string description, Func<T, (bool valid, string errorMessage)>? validatorFunc = null)
    {
        Option<T> option;
        if (aliases.Length > 1)
        {
            option = new(aliases[0], aliases[1..]);
        }
        else
        {
            option = new(aliases[0]);
        }

        option.Description = description;
        option.DefaultValueFactory = _ => defaultValueFactory();

        if (validatorFunc != null)
        {
            option.Validators.Add(result =>
            {
                var value = result.GetRequiredValue(option);
                var (valid, errorMessage) = validatorFunc(value);
                if (!valid)
                {
                    result.AddError($"Error in option '{option.Name}': {errorMessage}");
                }
            });
        }
        return option;
    }

    public static Argument<T> CreateArgument<T>(string name, string description, Func<T, (bool valid, string errorMessage)>? validatorFunc = null)
    {
        Argument<T> argument = new(name)
        {
            Description = description
        };

        if (validatorFunc != null)
        {
            argument.Validators.Add(result =>
            {
                var value = result.GetRequiredValue(argument);
                var (valid, errorMessage) = validatorFunc(value);
                if (!valid)
                {
                    result.AddError(errorMessage);
                }
            });
        }
        return argument;
    }
}
